""" This is a simple Python 3 script that takes a photo from a
picamera and posts it to an AWS S3 bucket
"""

import picamera
import tinys3
import configparser
import time
import os
from datetime import timedelta

config = configparser.ConfigParser()
aws_config_key = 'aws'
cam_upload_config_key = 'camupload'

config.read('camUpload.ini')

S3_ACCESS_KEY = config[aws_config_key]['AccessID']
S3_SECRET_KEY = config[aws_config_key]['SecretKey']
BUCKET_TARGET = config[aws_config_key]['BucketTarget']

conn = tinys3.Connection(S3_ACCESS_KEY, S3_SECRET_KEY, tls=True)

print("Initializing PiCamera")

camera = picamera.PiCamera()
image_file = config[cam_upload_config_key]['TempFileName']
s3_path_prefix = config[cam_upload_config_key]['S3PathPrefix']
days_to_expire = timedelta(days=int(config[cam_upload_config_key]['DaysToExpire']))

try:
    print("Capturing image")
    camera.capture(image_file)
    print("Captured, now uploading")

    epoch_time = int(time.time())

    f = open(image_file,'rb')
    conn.upload('{}{:d}cam.jpg'.format(s3_path_prefix, epoch_time),f, bucket=BUCKET_TARGET, expires=days_to_expire)
    print("Upload complete")
finally:
    os.remove(image_file)
