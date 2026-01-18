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

## GCP Deployment Guide

### 1. Configure Firewall Rules

Create the following **Ingress** firewall rules in **VPC Network → Firewall**:

| Name            | Port     | Purpose         |
| --------------- | -------- | --------------- |
| allow-mqtt-1883 | TCP 1883 | MQTT Broker     |
| allow-http-5000 | TCP 5000 | Flask Dashboard |

Source range: `0.0.0.0/0`

---

### 2. Create VM Instance

* Machine Type: `e2-micro`
* OS: Ubuntu 20.04 / 22.04 LTS
* Disk Size: 10 GB
* Enable HTTP/HTTPS traffic

---

### 3. VM Environment Setup (SSH)

```bash
sudo apt-get update
sudo apt-get install -y mosquitto mosquitto-clients python3-pip git mongodb

# Clone repository
git clone https://github.com/Dershyani/CPC357_ASSIGNMENT_2.git
cd CPC357_ASSIGNMENT_2

# Configure Mosquitto
sudo nano /etc/mosquitto/mosquitto.conf
```

Add:

```
listener 1883
allow_anonymous true
```

```bash
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

pip3 install -r requirements.txt
```

---

### 4. Run the System (3 Terminals)

**Terminal 1 – MQTT Subscriber (optional monitoring)**

```bash
mosquitto_sub -t "smartbin/#" -v
```

**Terminal 2 – Start Simulator**

```bash
python3 simulator.py
```

**Terminal 3 – Start Dashboard Backend**

```bash
python3 dashboard.py
```

---

### 5. Access Dashboard

Open a browser and navigate to:

```
http://<VM_EXTERNAL_IP>:5000
```

---

## Group Members

* **Dershyani A/P B. Thessaruva** – 164062
* **Lithia A/P Kisnen** – 163850

