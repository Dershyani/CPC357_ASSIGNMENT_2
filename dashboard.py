#!/usr/bin/env python3
from flask import Flask, jsonify, render_template, request
import json
import paho.mqtt.client as mqtt
import threading
from datetime import datetime
from collections import deque, OrderedDict
from pymongo import MongoClient
import time
import os

app = Flask(__name__)

# MongoDB connection
try:
    mongo_client = MongoClient('mongodb://localhost:27017/')
    db = mongo_client['smartbin_db']
    collection = db['bin_readings']
    print("✓ MongoDB connected successfully")
except Exception as e:
    print(f"⚠ MongoDB connection failed: {e}")
    collection = None

# Memory storage
bin_data = OrderedDict()
BIN_ORDER = ["BIN_001", "BIN_002", "BIN_003", "BIN_004", "BIN_005"]
LOCATIONS = ["CS Building", "Library", "Cafe", "Parking", "Hostel"]
bin_history = {bin_id: deque(maxlen=20) for bin_id in BIN_ORDER}

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        bin_id = data['bin_id']
        
        # Add icon if missing
        if 'icon' not in data:
            fill = data.get('fill_level', 0)
            if fill < 30:
                data['icon'] = '🟢'
            elif fill < 70:
                data['icon'] = '🟡'
            elif fill < 90:
                data['icon'] = '🟠'
            else:
                data['icon'] = '🔴'
        
        data['received'] = datetime.now().strftime('%H:%M:%S')
        
        # Store in memory
        bin_data[bin_id] = data
        bin_history[bin_id].append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'fill_level': data['fill_level'],
            'timestamp': time.time() * 1000
        })
        
        # Save to MongoDB
        if collection:
            try:
                collection.insert_one({
                    'bin_id': bin_id,
                    'location': data['location'],
                    'fill_level': data['fill_level'],
                    'status': data['status'],
                    'timestamp': datetime.now()
                })
                print(f"✓ {bin_id}: {data['fill_level']}% (saved to DB)")
            except Exception as e:
                print(f"✗ {bin_id}: DB error")
        else:
            print(f"✓ {bin_id}: {data['fill_level']}%")
            
    except Exception as e:
        print(f"Error: {e}")

def mqtt_thread():
    try:
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_message = on_message
        client.connect("localhost", 1883, 60)
        client.subscribe("smartbin/live")
        print("✓ MQTT connected successfully")
        client.loop_forever()
    except Exception as e:
        print(f"✗ MQTT connection failed: {e}")

threading.Thread(target=mqtt_thread, daemon=True).start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    bins = []
    
    for bin_id in BIN_ORDER:
        if bin_id in bin_data:
            b = bin_data[bin_id]
        else:
            b = {
                'bin_id': bin_id,
                'location': LOCATIONS[BIN_ORDER.index(bin_id)],
                'fill_level': 0,
                'status': 'OFFLINE',
                'icon': '⚫',
                'received': '--:--:--',
                'timestamp': '--:--:--'
            }
        
        status = b['status']
        status_class = status.lower() if status in ['LOW', 'MODERATE', 'HIGH', 'OVERFLOW', 'offline'] else 'moderate'
        
        bins.append({
            'id': b['bin_id'],
            'location': b['location'],
            'fill': b['fill_level'],
            'status': status,
            'icon': b.get('icon', '🗑️'),
            'status_class': status_class,
            'time': b.get('received', b.get('timestamp', '--:--:--'))
        })
    
    active_bins = [b for b in bins if b['status'] != 'OFFLINE']
    
    if active_bins:
        total = len(active_bins)
        avg = sum(b['fill'] for b in active_bins) / total
        full = sum(1 for b in active_bins if b['fill'] > 70)
    else:
        total = avg = full = 0
    
    return jsonify({
        'total': len(bins),
        'avg': round(avg, 1),
        'full': full,
        'bins': bins
    })

@app.route('/api/history')
def api_history():
    history = OrderedDict()
    for bin_id in BIN_ORDER:
        if bin_id in bin_history:
            history[bin_id] = list(bin_history[bin_id])[-10:]
        else:
            history[bin_id] = []
    
    return jsonify(history)

@app.route('/api/db/stats')
def db_stats():
    if not collection:
        return jsonify({'error': 'Database not available'})
    
    try:
        count = collection.count_documents({})
        bins = collection.distinct('bin_id')
        
        return jsonify({
            'total_readings': count,
            'bins': bins,
            'status': 'connected'
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/db/recent')
def db_recent():
    if not collection:
        return jsonify({'error': 'Database not available'})
    
    try:
        limit = request.args.get('limit', 10, type=int)
        data = list(collection.find(
            {},
            {'_id': 0, 'bin_id': 1, 'location': 1, 'fill_level': 1, 'status': 1}
        ).sort('_id', -1).limit(limit))
        
        return jsonify({'recent': data})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/db/history/<bin_id>')
def db_history(bin_id):
    if not collection:
        return jsonify({'error': 'Database not available'})
    
    try:
        limit = request.args.get('limit', 10, type=int)
        data = list(collection.find(
            {'bin_id': bin_id},
            {'_id': 0, 'bin_id': 1, 'location': 1, 'fill_level': 1, 'status': 1}
        ).sort('_id', -1).limit(limit))
        
        return jsonify({'readings': data})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 SMART BIN DASHBOARD WITH MONGODB")
    print("=" * 60)
    print("Access: http://136.112.221.13:5000")
    print("API Endpoints:")
    print("  /api/data           - Live data")
    print("  /api/db/stats       - Database stats")
    print("  /api/db/recent      - Recent readings")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
