'''
Author: Manntresh khurana
Repository:
Date: 10-03-2025
Description: This is the main file for the AI Traffic Signal Control System.
'''

import cv2
import numpy as np
from ultralytics import YOLO
import requests
import googlemaps
from flask import Flask, request, jsonify
from geopy.distance import geodesic


# GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
# gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


model = YOLO("yolov8n.pt")


app = Flask(__name__)


ambulance_data = {}


RED = (0, 0, 255)
GREEN = (0, 255, 0)


traffic_light = RED


TRAFFIC_SIGNAL_LOCATION = (40.758896, -73.985130)  


@app.route("/update_gps", methods=["POST"])
def update_gps():
    global ambulance_data
    data = request.json
    ambulance_id = data["ambulance_id"]
    gps_location = (data["latitude"], data["longitude"])
    ambulance_data[ambulance_id] = gps_location
    return jsonify({"status": "updated", "ambulance_id": ambulance_id, "location": gps_location})


def is_ambulance_near(ambulance_gps):
    response = gmaps.distance_matrix(
        origins=[ambulance_gps],
        destinations=[TRAFFIC_SIGNAL_LOCATION],
        mode="driving"
    )
    distance_meters = response["rows"][0]["elements"][0]["distance"]["value"]
    return distance_meters < 200  


def get_fastest_route(ambulance_gps, hospital_gps):
    directions = gmaps.directions(
        origin=ambulance_gps,
        destination=hospital_gps,
        mode="driving",
        alternatives=True  
    )
    return directions[0]["legs"][0]["duration"]["text"], directions[0]["legs"][0]["distance"]["text"]


def change_traffic_light(ambulance_near):
    global traffic_light
    if ambulance_near:
        traffic_light = GREEN  
    else:
        traffic_light = RED  


def draw_traffic_light(frame):
    light_color = traffic_light
    cv2.circle(frame, (50, 50), 30, light_color, -1)


def measure_traffic_density(frame):
    results = model(frame)
    vehicle_count = 0

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            if class_id in [2, 3, 5, 7]:  
                vehicle_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)

    return vehicle_count


cap = cv2.VideoCapture("traffic_video.mp4") # Use 0 for webcam e.g. cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    queue_length = measure_traffic_density(frame)  

    ambulance_near = False
    for ambulance_id, ambulance_gps in ambulance_data.items():
        if is_ambulance_near(ambulance_gps):
            ambulance_near = True
            hospital_gps = (40.748817, -73.985428)  
            eta, distance = get_fastest_route(ambulance_gps, hospital_gps)
            print(f"🚑 Ambulance {ambulance_id} → ETA to Hospital: {eta}, Distance: {distance}")

    
    change_traffic_light(ambulance_near)

    
    draw_traffic_light(frame)

    
    cv2.imshow("AI Traffic Signal Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()