import logging
import signal
import os
import time
import requests

from influxdb_client import InfluxDBClient, Point
from lywsd03mmc import Lywsd03mmcClient



# 🔹 Logging-Konfiguration mit API-Post
Golang_API_URL = "http://localhost:8080/log"
def send_log(record):
    try:
        requests.post(Golang_API_URL, json={"message": record})
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Senden des Logs: {e}")

api_loghandler = logging.Handler()
api_loghandler.emit = lambda record: send_log(api_loghandler.format(record))


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        api_loghandler
    ]
)

# 🔹 InfluxDB Konfiguration
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "mytoken")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my_org")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "my_bucket")

# 🔹 InfluxDB Initialisierung
influxClient = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influxClient.write_api()

# 🔹 Sensor Konfiguration
SENSOR_MAC = "A4:C1:38:5C:A1:0B"
sensorClient = Lywsd03mmcClient(SENSOR_MAC)

# 🔹 Flag für sauberes Beenden
running = True

# 🔹 Signal-Handler für SIGINT & SIGTERM
def shutdown_handler(signum, frame):
    global running
    logging.info(f"🛑 Signal {signum} empfangen. Beende Skript...")
    running = False

# Signale registrieren
signal.signal(signal.SIGINT, shutdown_handler)  # CTRL+C (SIGINT)
signal.signal(signal.SIGTERM, shutdown_handler)  # Docker Stop (SIGTERM)

def sensor_loop():
    while running:
        try:
            temperature, humidity, battery = sensorClient.temperature, sensorClient.humidity, sensorClient.battery
            logging.info(f"\n🌡️ Temperatur: {temperature:.1f}℃ \n💧 Luftfeuchtigkeit: {humidity:.1f}% \n🔋 Spannung: {battery:.1f}")

            point = (
                Point("sensor_data")
                .field("temperature", temperature)
                .field("humidity", humidity)
                .field("battery", battery)
            )

            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

        except Exception as e:
            logging.error(f"⚠️ Fehler beim Lesen der Sensordaten: {e}")

        time.sleep(5)

# 🔹 Sensor-Loop starten
sensor_loop()

# 🔹 Cleanup beim Beenden
logging.info("🛑 Datenlogger gestoppt. Schließe Verbindungen...")
influxClient.close()
logging.info("✅ Skript erfolgreich beendet.")

logger = logging.getLogger()
logger.info("Test test log log")
