import sqlite3
import folium
import json
import os
import glob
import datetime
import math
import collections
import logging
import argparse

# Constants
DEVICE_TYPE_MAPPING = {
    'Wi-Fi AP': 'wifi_ap',
    'Wi-Fi client': 'wifi_client',
    'Bluetooth': 'bluetooth',
    'ADS-B': 'adsb',
    'drone': 'drone'
}

known_drone_mac_prefixes = ['60:60:1F', '90:3A:E6']
known_drone_ssids = ['DJI', 'Parrot']

# Functions
def detect_snoopers(device_detections, movement_threshold):
    snoopers = []
    for mac, detections in device_detections.items():
        total_distance = 0
        for i in range(1, len(detections)):
            lon1, lat1 = detections[i-1]['lon'], detections[i-1]['lat']
            lon2, lat2 = detections[i]['lon'], detections[i]['lat']
            distance = haversine(lon1, lat1, lon2, lat2)
            total_distance += distance
            if distance > movement_threshold:
                snoopers.append({
                    'mac': mac,
                    'total_distance': total_distance,
                    'detections': detections
                })
                break
    return snoopers

def extract_alerts_from_kismet(kismet_file):
    alerts = []
    conn = sqlite3.connect(kismet_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts")
    for row in cursor.fetchall():
        alert = {
            'message': row[1],
            'type': row[2],
            'lat': row[3],
            'lon': row[4]
        }
        alerts.append(alert)
    conn.close()
    return alerts

def extract_device_detections(kismet_file):
    device_detections = collections.defaultdict(list)
    conn = sqlite3.connect(kismet_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices")
    for row in cursor.fetchall():
        detection = {
            'mac': row[1],
            'type': row[2],
            'lat': row[3],
            'lon': row[4],
            'timestamp': row[5],
            'name': row[6],
            'encryption': row[7]
        }
        device_detections[row[1]].append(detection)
    conn.close()
    return device_detections

def find_most_recent_kismet_file(directory):
    kismet_files = glob.glob(os.path.join(directory, '*.kismet'))
    if not kismet_files:
        return None
    most_recent_file = max(kismet_files, key=os.path.getmtime)
    return most_recent_file

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    miles = 3956 * c
    return miles

def is_drone(ssid, mac_address):
    if any(ssid.startswith(prefix) for prefix in known_drone_ssids):
        return True
    if any(mac_address.startswith(prefix) for prefix in known_drone_mac_prefixes):
        return True
    return False

def is_valid_lat_lon(lat, lon):
    return -90 <= lat <= 90 and -180 <= lon <= 180

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process Kismet database files.')
    parser.add_argument('directory', type=str, help='Directory containing Kismet database files')
    parser.add_argument('--output', type=str, default='output_map.html', help='Output HTML map file')
    parser.add_argument('--threshold', type=float, default=0.05, help='Movement threshold in miles for snooper detection')
    return parser.parse_args()

def sanitize_string(s):
    return s.replace('{{', '{ {').replace('}}', '} }')

def visualize_devices_snoopers_and_alerts(device_detections, snoopers, alerts, output_map_file):
    m = folium.Map(location=[0, 0], zoom_start=2)
    for mac, detections in device_detections.items():
        for detection in detections:
            if is_valid_lat_lon(detection['lat'], detection['lon']):
                folium.Marker(
                    location=[detection['lat'], detection['lon']],
                    popup=sanitize_string(json.dumps(detection)),
                    icon=folium.Icon(color='blue' if detection['type'] == 'Wi-Fi AP' else 'green')
                ).add_to(m)
    for snooper in snoopers:
        points = [(d['lat'], d['lon']) for d in snooper['detections'] if is_valid_lat_lon(d['lat'], d['lon'])]
        folium.PolyLine(points, color='red').add_to(m)
    for alert in alerts:
        if is_valid_lat_lon(alert['lat'], alert['lon']):
            folium.Marker(
                location=[alert['lat'], alert['lon']],
                popup=sanitize_string(json.dumps(alert)),
                icon=folium.Icon(color='red', icon='exclamation-sign')
            ).add_to(m)
    m.save(output_map_file)

def main():
    args = parse_arguments()
    kismet_file = find_most_recent_kismet_file(args.directory)
    if not kismet_file:
        logging.error('No Kismet files found in the specified directory.')
        return
    device_detections = extract_device_detections(kismet_file)
    snoopers = detect_snoopers(device_detections, args.threshold)
    alerts = extract_alerts_from_kismet(kismet_file)
    visualize_devices_snoopers_and_alerts(device_detections, snoopers, alerts, args.output)

if __name__ == '__main__':
    main()