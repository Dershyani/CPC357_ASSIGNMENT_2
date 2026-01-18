# CPC357: Smart Bin Monitoring System

A cloud-based IoT application for real-time monitoring of waste bin fill levels using MQTT communication, Flask backend services, MongoDB storage, and an interactive web dashboard deployed on Google Cloud Platform (GCP).

This project is developed as part of **CPC357 – IoT Architecture and Smart Applications** (Assignment 2).

---

## Technology Stack

| Component          | Technology                      |
| ------------------ | ------------------------------- |
| IoT Simulation     | Python                          |
| Data Communication | MQTT (Mosquitto, paho-mqtt)     |
| Backend Server     | Flask                           |
| Database           | MongoDB (pymongo)               |
| Frontend           | HTML, CSS, JavaScript, Chart.js |
| Cloud Platform     | Google Cloud Platform (GCP)     |

---

## Cloud Environment Setup

### VM Configuration:
- Machine Type: `e2-micro`
- Boot Disk: 10GB, Ubuntu 20.04 LTS
- Firewall Rules: Allow HTTP and HTTPS traffic

#### Firewall Configuration:
1. **Access Firewall Settings** in Google Cloud Console
2. **Create New Rule** with these parameters:
      - Name: allow-mqtt-flask
      - Network: default
      - Priority: 1000
      - Direction: Ingress
      - Action: Allow
      - Targets: All instances in network
      - Source IP ranges: 0.0.0.0/0
      - Protocols/Ports : tcp(1883,5000,9001)
---

## Environment Setup

### 1. Once the VM is running, connect via SSH to set up the development environment.

### 2. Update system packages and install dependencies:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip git -y
```

### 3. Install the MQTT broker (Mosquitto) and ensure it is running:

```bash
sudo apt install -y mosquitto
sudo systemctl start mosquitto
sudo systemctl enable mosquitto
systemctl status mosquitto
```

### 4. Clone the project repository:

```bash
git clone https://github.com/Dershyani/CPC357_ASSIGNMENT_2.git
cd CPC357_ASSIGNMENT_2
```

### 5. Install Python dependencies:

```bash
pip3 install -r requirements.txt
```

### 6. The system uses MongoDB to store historical bin readings, so install MongoDB:

```bash
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### 7. Running the IoT Simulation:

The smart bin system is simulated using the simulator.py script, which acts as both the sensor and the ESP32 microcontroller. The simulator generates fill-level data for each bin every 10 seconds and publishes it via MQTT.

### 8. Open a new SSH session, and start the simulator:

```bash
cd CPC357_ASSIGNMENT_2
python3 simulator.py
```

### 9. Running the Dashboard Backend:

The Flask server processes incoming MQTT messages, stores data in MongoDB, and serves the live dashboard.

### 10. Open a second SSH session, and start the Flask server:

```bash
cd CPC357_ASSIGNMENT_2
python3 dashboard.py
```

The server subscribes to MQTT topics, updates in-memory data, and exposes RESTful APIs for live and historical data.

### 11. Access the dashboard via a browser at:

```
http://<VM_EXTERNAL_IP>:5000
```

---

## Group Members

* **Dershyani A/P B. Thessaruva** – 164062
* **Lithia A/P Kisnen** – 163850
