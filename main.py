import datetime
import ssl
import paho.mqtt.client as mqtt
import time
import os
import logging
import requests
import json

from dotenv import load_dotenv
load_dotenv()

class SimulatedDevice():
    def __init__(self):
        self.device_hub_url = os.getenv('DEVICE_HUB_URL')
        self.device_id = os.getenv('DEVICE_ID')
        self.device_primary_key = os.getenv('DEVICE_PRIMARY_KEY')

    def getMqttCreds(self):
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
    

    def pubMessage(self):
        mqtt_creds_object = self.getMqttCreds()
        if(mqtt_creds_object):
            mqtt_client_id = mqtt_creds_object.get('mqtt_client_id')
            mqtt_username = mqtt_creds_object.get('mqtt_username')
            mqtt_password = mqtt_creds_object.get('mqtt_password')
            mqtt_host = mqtt_creds_object.get('mqtt_host')
            mqtt_pub_topic = mqtt_creds_object.get('mqtt_pub_topic')
            mqtt_sub_topic = mqtt_creds_object.get('mqtt_sub_topic')
            mqtt_host = mqtt_creds_object.get('mqtt_host')
        
            client = mqtt.Client(client_id=mqtt_client_id)
            client.username_pw_set(mqtt_username,mqtt_password)




if __name__ == '__main__':
    smd = SimulatedDevice()
    print(smd.getMqttCreds())

