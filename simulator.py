#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1883, 60)

bins = ["BIN_001", "BIN_002", "BIN_003", "BIN_004", "BIN_005"]
locations = ["CS Building", "Library", "Cafe", "Parking", "Hostel"]

print("=" * 50)
print("Smart Bin Simulator")
print("=" * 50)
print("Sending data every 10 seconds")
print("Press Ctrl+C to stop")
print("=" * 50)

counter = 0
try:
    while True:
        counter += 1
        print(f"\n📦 CYCLE {counter} - {time.strftime('%H:%M:%S')}")
        print("-" * 40)
        
        for i in range(5):
            fill = random.randint(0, 100)
            
            if fill < 30:
                status = "LOW"
                icon = "🟢"
            elif fill < 70:
                status = "MODERATE"
                icon = "🟡"
            elif fill < 90:
                status = "HIGH"
                icon = "🟠"
            else:
                status = "OVERFLOW"
                icon = "🔴"
            
            data = {
                "bin_id": bins[i],
                "location": locations[i],
                "fill_level": fill,
                "status": status,
                "icon": icon,
                "timestamp": time.strftime("%H:%M:%S"),
                "cycle": counter
            }
            
            client.publish("smartbin/live", json.dumps(data))
            print(f"{icon} {bins[i]}: {fill}%")
            
            time.sleep(0.5)
        
        print("-" * 40)
        print(f"⏰ Next update in 10 seconds...")
        time.sleep(10)
        
except KeyboardInterrupt:
    print("\n\n" + "=" * 50)
    print("Simulator stopped")
    print("=" * 50)
finally:
    client.disconnect()
