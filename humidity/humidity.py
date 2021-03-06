""" This is a simple Python 3 script that takes a photo from a
picamera and posts it to an AWS S3 bucket
"""

import configparser
import time
import os
import os.path
from datetime import timedelta
import json
import datetime
import requests
import Adafruit_DHT

def main():
    config = configparser.ConfigParser()
    aws_config_key = 'aws'

    config.read('humidity.ini')

    API_KEY = config[aws_config_key]['APIKey']
    GPIO_PIN = config[aws_config_key]['GPIOPin']
    REST_URL = config[aws_config_key]['RestUrl']
    SENSOR_ID = config[aws_config_key]['SensorID']

    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, GPIO_PIN)
    #humidity = 0.2
    datetime = int(round(time.time() * 1000))
    payload = json.dumps({'sensor_id': SENSOR_ID, 'humidity': humidity, 'datetime': datetime})
    print('Sending payload to server {}'.format(payload))
    r = requests.post(REST_URL, headers={'x-api-key': API_KEY, 'Accept': 'application/json', 'Content-type': 'application/json'}, data=payload)
    print('Return code {}'.format(r.status_code))
main()
