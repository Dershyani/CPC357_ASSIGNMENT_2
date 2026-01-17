# 🗑️ Smart Bin Monitoring System

A real-time smart bin monitoring system built with Python, MQTT, and Flask.  
This IoT application simulates multiple smart bins with varying fill levels and displays them on a live dashboard.

Project Structure
smart-bin-monitoring/
├── simulator.py          # MQTT publisher
├── dashboard.py          # Flask dashboard
├── README.md             # Documentation
└── requirements.txt      # Dependencies



## GCP Deployment

### 1. Create VM Instance

- **Machine Type**: e2-micro  
- **Boot Disk**: 10GB, Ubuntu 20.04 LTS  
- **Firewall**: Allow HTTP & HTTPS traffic

### 2. Setup Commands (GCP SSH)

```bash
# Update system
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git mosquitto mosquitto-clients

# Clone project
git clone https://github.com/Dershyani/CPC357_ASSIGNMENT_2.git
cd CPC357_ASSIGNMENT_2

create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
# or
pip install flask paho-mqtt

Run the Smart Bin System
# Start MQTT Broker
sudo systemctl start mosquitto

# In separate terminal, run simulator
python3 simulator.py

# In another terminal, run dashboard
python3 dashboard.py

Open a browser and go to:
http://<YOUR_VM_EXTERNAL_IP>:5000
```
Project Features

Real-time Monitoring: Live updates every 10 seconds

Visual Status Indicators: Color-coded status with emojis

🟢 LOW (0-29%)

🟡 MODERATE (30-69%)

🟠 HIGH (70-89%)

🔴 OVERFLOW (90-100%)

Responsive Dashboard: Clean web interface with progress bars

MQTT Integration: Lightweight messaging protocol

System Metrics: Total bins, average fill, bins needing emptying

Automatic Updates: No page refresh needed

MQTT Topics

Topic: smartbin/live

Message Format (JSON):

{
    "bin_id": "BIN_001",
    "location": "CS Building",
    "fill_level": 85,
    "status": "HIGH",
    "icon": "🟠",
    "timestamp": "15:38:34"
}


Group Members

Dershyani A/P B.Thessaruva - 164062

Lithia A/P Kisnen - 163850
