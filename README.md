# CPC357 Assignment 2 - Smart Bin IoT Application

## Project Overview
This project is a **Smart Bin monitoring system** developed as part of the CPC357 IoT course assignment.  
It demonstrates a working IoT application where multiple bins are monitored in real-time.  

The system includes:
- A **simulator** to generate bin fill-level data.
- A **Flask web dashboard** to display live data.
- Communication using **MQTT** protocol.

The main goal is to showcase IoT concepts including data collection, real-time monitoring, and cloud/internet-connected visualization (simulated locally using Python).

---

## Features
- Simulates **five Smart Bins** with unique IDs and locations.
- Real-time monitoring of bin fill levels.
- **Color-coded status** indicators:
  - 🟢 LOW (0-29%)
  - 🟡 MODERATE (30-69%)
  - 🟠 HIGH (70-89%)
  - 🔴 OVERFLOW (90-100%)
- Dashboard metrics:
  - Total bins
  - Average fill percentage
  - Number of bins that need emptying (fill > 70%)
- Live update every 10 seconds.
- Dashboard table with last update timestamp for each bin.

---
## How to Run

1. Start the MQTT broker locally:
```bash
mosquitto
