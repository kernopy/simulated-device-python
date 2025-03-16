import datetime
import ssl
import paho.mqtt.client as mqtt
import time
import os
import logging
import requests
import json
import random

from dotenv import load_dotenv
load_dotenv()

class SimulatedDevice():
    def __init__(self):
        self.device_hub_url = os.getenv('DEVICE_HUB_URL')
        self.device_id = os.getenv('DEVICE_ID')
        self.device_primary_key = os.getenv('DEVICE_PRIMARY_KEY')
        self.max_messages = os.getenv('MAX_MESSAGES')
        self.time_delay = os.getenv('TIME_DELAY')
        self.device_config = {}

    def getDeviceCreds(self):
        try:
            # Prepare the request payload
            payload = {
                "device_unique_id": self.device_id,
                "primary_key": self.device_primary_key
            }
            
            # Make the POST request
            response = requests.post(
                self.device_hub_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Return the JSON response as a dictionary
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting MQTT credentials: {str(e)}")
            return None
    
    # Callback when the client connects to the broker
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    # Callback when the client disconnects
    def on_disconnect(self,client, userdata, rc):
        print("Disconnected from MQTT Broker",rc)

    # Callback when a message is received
    def on_message(self,client, userdata, msg):
        print(f"Received message from {msg.topic}: {msg.payload.decode()}")

    def pubMessage(self):
        mqtt_creds_object = self.getDeviceCreds()
        self.device_config=mqtt_creds_object.get('device_config_json')
        if(mqtt_creds_object):
            mqtt_client_id = mqtt_creds_object.get('device_mqtt_details').get('mqtt_client_id')
            mqtt_username = mqtt_creds_object.get('device_mqtt_details').get('mqtt_username')
            mqtt_password = mqtt_creds_object.get('device_mqtt_details').get('mqtt_password')
            mqtt_host = mqtt_creds_object.get('device_mqtt_details').get('mqtt_host')
            mqtt_pub_topic = mqtt_creds_object.get('device_mqtt_details').get('mqtt_pub_topic')
            mqtt_sub_topic = mqtt_creds_object.get('device_mqtt_details').get('mqtt_sub_topic')
            mqtt_host = mqtt_creds_object.get('device_mqtt_details').get('mqtt_host')
        
            client = mqtt.Client(client_id=mqtt_client_id)
            client.username_pw_set(mqtt_username,mqtt_password)

            # Enable TLS (if required)
            client.tls_set(cert_reqs=ssl.CERT_NONE)  # Use 'ssl.CERT_REQUIRED' with a CA certificate for security

            # Assign callbacks
            client.on_connect = self.on_connect
            client.on_disconnect = self.on_disconnect
            client.on_message = self.on_message

            # Connect to MQTT broker
            client.connect(mqtt_host, 8883, 60)
            client.loop_start()
            for i in range(int(self.max_messages)):
                dataPacket = self.generateMessageData()
                message = json.dumps(dataPacket)
                result = client.publish(mqtt_pub_topic,message,qos=1)
                # Check if publish was successful
                if result[0] == 0:
                    print(f"Message published successfully: {message}")
                else:
                    print(f"Failed to publish message")
                time.sleep(int(self.time_delay))
            
            client.loop_stop()
            client.disconnect
    
    def generateMessageData(self):
        current_ts = datetime.datetime.now().isoformat()
        paramList= self.device_config.get('parameterConfig')
        dataPacket={}
        paramPacketList=[]
        dataPacket['edge_ts']=current_ts
        for param in paramList:
            paramPacket = {
                'parameter':param.get('name'),
                'value':round(random.uniform(0, 100))
            }
            paramPacketList.append(paramPacket)
        dataPacket['data']=paramPacketList
        return dataPacket





if __name__ == '__main__':
    smd = SimulatedDevice()
    print(smd.pubMessage())

