""" This is a simple Python 3 script that takes a photo from a
picamera and posts it to an AWS S3 bucket
"""

import picamera
import tinys3
import configparser
import time
import os

config = configparser.ConfigParser()
config.read('camUpload.ini')
S3_ACCESS_KEY = config['aws']['AccessID']
S3_SECRET_KEY = config['aws']['SecretKey']
BUCKET_TARGET = config['aws']['BucketTarget']
conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY,tls=True)

print("Initializing PiCamera")

camera = picamera.PiCamera()
image_file = config['camupload']['TempFileName']
s3_path_prefix = config['camupload']['S3PathPrefix']

try:
    print("Capturing image")
    camera.capture(image_file)
    print("Captured, now uploading")

    epoch_time = int(time.time())

    f = open(image_file,'rb')
    conn.upload('{}{:d}cam.jpg'.format(s3_path_prefix, epoch_time),f, bucket=BUCKET_TARGET)
    print("Upload complete")
finally:
    os.remove(image_file)
