#!/usr/bin/env python3
from flask import Flask, jsonify, render_template_string
import json
import paho.mqtt.client as mqtt
import threading
from datetime import datetime

app = Flask(__name__)
bin_data = {}

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        bin_id = data['bin_id']
        bin_data[bin_id] = data
        bin_data[bin_id]['received'] = datetime.now().strftime('%H:%M:%S')
        print(f"✓ {bin_id}: {data['fill_level']}%")
    except:
        pass

def mqtt_thread():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.subscribe("smartbin/live")
    client.loop_forever()

threading.Thread(target=mqtt_thread, daemon=True).start()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Bin Live Dashboard</title>
    <style>
        body { font-family: Arial; margin: 30px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #2E7D32; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }
        .metrics { display: flex; gap: 20px; margin: 20px 0; }
        .metric-box { flex: 1; background: #4CAF50; color: white; padding: 15px; border-radius: 8px; text-align: center; }
        .metric-value { font-size: 28px; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { background: #4CAF50; color: white; padding: 12px; }
        td { padding: 10px; border-bottom: 1px solid #ddd; }
        .progress { background: #e0e0e0; height: 20px; border-radius: 4px; overflow: hidden; }
        .fill { background: #4CAF50; height: 100%; color: white; text-align: center; font-size: 12px; }
        .low { color: #4CAF50; }
        .moderate { color: #FFC107; }
        .high { color: #FF9800; }
        .overflow { color: #F44336; }
    </style>
    <script>
    async function updateDashboard() {
        const response = await fetch('/api/data');
        const data = await response.json();
        
        // Update metrics
        document.getElementById('totalBins').textContent = data.total;
        document.getElementById('avgFill').textContent = data.avg.toFixed(1) + '%';
        document.getElementById('fullBins').textContent = data.full;
        
        // Update table
        let tableBody = document.getElementById('binTable');
        tableBody.innerHTML = '';
        
        data.bins.forEach(bin => {
            let row = tableBody.insertRow();
            row.innerHTML = `
                <td><strong>${bin.icon} ${bin.id}</strong></td>
                <td>${bin.location}</td>
                <td>
                    <div class="progress">
                        <div class="fill" style="width: ${bin.fill}%">${bin.fill}%</div>
                    </div>
                </td>
                <td class="${bin.status_class}"><strong>${bin.status}</strong></td>
                <td>${bin.time}</td>
            `;
        });
    }
    
    // Update every 10 seconds
    setInterval(updateDashboard, 10000);
    window.onload = updateDashboard;
    </script>
</head>
<body>
    <div class="container">
        <h1>🗑️ Smart Bin Monitoring System</h1>
        <p>CPC357 IoT Assignment - Live Data Dashboard</p>
        
        <div class="metrics">
            <div class="metric-box">
                <div>Total Bins</div>
                <div class="metric-value" id="totalBins">0</div>
            </div>
            <div class="metric-box">
                <div>Average Fill</div>
                <div class="metric-value" id="avgFill">0%</div>
            </div>
            <div class="metric-box">
                <div>Need Emptying</div>
                <div class="metric-value" id="fullBins">0</div>
            </div>
        </div>
        
        <h2>📊 Live Bin Status</h2>
        <table>
            <thead>
                <tr>
                    <th>Bin ID</th>
                    <th>Location</th>
                    <th>Fill Level</th>
                    <th>Status</th>
                    <th>Last Update</th>
                </tr>
            </thead>
            <tbody id="binTable">
                <tr><td colspan="5" style="text-align:center;">Loading data from MQTT...</td></tr>
            </tbody>
        </table>
        
        <div style="margin-top: 30px; padding: 15px; background: #f8f9fa; border-radius: 5px;">
            <p><strong>System Status:</strong> 
                <span style="color: #4CAF50;">✓ MQTT Connected</span> | 
                <span style="color: #4CAF50;">✓ Simulator Running</span> | 
                <span style="color: #4CAF50;">✓ Dashboard Active</span>
            </p>
            <p><em>Data updates automatically every 10 seconds</em></p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/data')
def api_data():
    bins = list(bin_data.values())
    
    if not bins:
        return jsonify({
            'total': 0,
            'avg': 0,
            'full': 0,
            'bins': []
        })
    
    total = len(bins)
    avg = sum(b['fill_level'] for b in bins) / total
    
    # Count bins with fill_level > 70 (HIGH and OVERFLOW)
    full = sum(1 for b in bins if b['fill_level'] > 70)
    
    formatted = []
    for b in bins:
        status = b['status']
        
        if status == "LOW":
            status_class = 'low'
        elif status == "MODERATE":
            status_class = 'moderate'
        elif status == "HIGH":
            status_class = 'high'
        elif status == "OVERFLOW":
            status_class = 'overflow'
        else:
            status_class = 'moderate'
        
        formatted.append({
            'id': b['bin_id'],
            'location': b['location'],
            'fill': b['fill_level'],
            'status': status,
            'icon': b.get('icon', '🗑️'),
            'status_class': status_class,
            'time': b['timestamp']
        })
    
    return jsonify({
        'total': total,
        'avg': round(avg, 1),
        'full': full,
        'bins': formatted
    })

if __name__ == '__main__':
    print("=" * 60)
    print("SMART BIN LIVE DASHBOARD")
    print("=" * 60)
    print("Access: http:// YOUR EXTERNAL VM IP:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False)
