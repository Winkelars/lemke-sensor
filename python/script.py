from influxdb_client import InfluxDBClient, Point
from lywsd03mmc import Lywsd03mmcClient
import os
import time

# 🔹 InfluxDB Konfiguration
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "mytoken")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my_org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "my_bucket")


influxClient = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influxClient.write_api()

# 🔹 Sensor Konfiguration (MAC-Adresse anpassen!)
SENSOR_MAC = "A4:C1:38:5C:A1:0B"
sensorClient = Lywsd03mmcClient(SENSOR_MAC)

def insert_sensor_data():
    while True:
        try:
            temperature, humidity, battery = sensorClient.temperature, sensorClient.humidity, sensorClient.battery
            print(f"🌡️ Temperatur: {temperature:.1f}°C, 💧 Luftfeuchtigkeit: {humidity:.1f}%, 🔋 Batterie: {battery}%")

            point = (
                Point("sensor_data")
                .field("temperature", temperature)
                .field("humidity", humidity)
                .field("battery", battery)
            )

            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

        except Exception as e:
            print(f"⚠️ Fehler beim Lesen der Sensordaten: {e}")

insert_sensor_data()
