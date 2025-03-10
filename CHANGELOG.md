# CHANGELOG

## [1.0.0] - 10-03-2025

### Added

### ✅ AI-Powered Traffic Signal Control

- [x] **YOLOv8 Integration** for real-time vehicle detection and traffic density measurement.
- [x] Dynamic traffic light control based on ambulance proximity.

### ✅ Ambulance Tracking & Routing

- [x] **GPS-based tracking** of ambulances using `/update_gps` API endpoint.
- [x] **Google Maps API integration** to check ambulance distance from traffic signals.
- [x] **Automated route optimization** for ambulances to the nearest hospital.

### ✅ Traffic Density Measurement

- [x] Uses **YOLOv8 object detection** to count vehicles at intersections.
- [x] **Dynamic signal adjustments** based on real-time traffic density.

### ✅ Video & Live Camera Feed Support

- [x] **Video File Input**: Process traffic video streams from MP4 files.
- [x] **Live Webcam Feed**: Support for real-time camera monitoring.

### ✅ Real-time Visualization

- [x] **Traffic light rendering** on video feed.
- [x] **Bounding boxes** for detected vehicles to analyze congestion levels.

### ✅ API & Backend Features

- [x] Flask API to receive and process **ambulance GPS data**.
- [x] Uses **Google Distance Matrix API** to determine ambulance proximity.
- [x] Dynamic response adjustments based on ambulance location and route ETA.
