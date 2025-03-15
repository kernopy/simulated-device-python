import datetime
import ssl
import paho.mqtt.client as mqtt
import time
import random

BROKER = "dev-cluster.kernopy.com"  # Replace with your MQTT broker
PORT = 8883  # MQTT over TLS/SSL
USERNAME = "global-admin-ws"  # Replace with your username
PASSWORD = "Global@123"  # Replace with your password
TOPIC = "kernopy/telemetry/device/733a6da0-73de-4e79-9bd7-72b10adf8389"

counter = 0

def get_message():
    global counter
    counter=counter+1
    return f'''
    {{
    "edge_ts":"{datetime.datetime.now().isoformat()}",
    "data":[
        {{
        "parameter":"Humidity",
        "value":{counter}
        }}
    ]
    }}'''


# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Publish message after connection
        # client.publish(TOPIC, MESSAGE)
    else:
        print(f"Failed to connect, return code {rc}")


# Callback when the client disconnects
def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker",rc)


# Callback when a message is received
def on_message(client, userdata, msg):
    global counter
    counter=counter+1
    print(counter)
    print(f"Received message from {msg.topic}: {msg.payload.decode()}")


# Initialize MQTT client
client = mqtt.Client(client_id=USERNAME)
client.username_pw_set(USERNAME, PASSWORD)

# Enable TLS (if required)
client.tls_set(cert_reqs=ssl.CERT_NONE)  # Use 'ssl.CERT_REQUIRED' with a CA certificate for security

# Assign callbacks
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to MQTT broker
client.connect(BROKER, PORT, 60)

# Start the MQTT client loop
client.loop_start()

# Wait for connection and then publish messages periodically
time.sleep(2)  # Allow time to establish connection
client.subscribe("#")

# Stop loop and disconnect after publishing
client.loop_forever()
# client.disconnect()