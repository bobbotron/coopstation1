""" This is a simple Python 3 script that takes a photo from a
picamera and posts it to an AWS S3 bucket
"""

import picamera
import tinys3
import configparser
import time
import os
import os.path
from datetime import timedelta
import json

RECENT_LOG = 'recent.log'

def update_log(entry):
    def read_recent_log():
        if os.path.isfile(RECENT_LOG):
            with open (RECENT_LOG, "r") as recent_log_file:
                return json.load(recent_log_file)
        else:
            return []
    def write_log(entries):
        with open (RECENT_LOG, "w") as log_file:
            json.dump(entries, log_file)
    cur_log = read_recent_log()
    cur_log.append(entry)
    while len(cur_log) > 10:
        del cur_log[0]
    write_log(cur_log)
    return cur_log

def main():
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

        with open (image_file, "rb") as f:
            s3_image_file_name = '{}{:d}cam.jpg'.format(s3_path_prefix, epoch_time)
            conn.upload(s3_image_file_name, f, bucket=BUCKET_TARGET, expires=days_to_expire)
        with open (RECENT_LOG, "rb") as f:
            s3_image_file_name = '{}log.json'.format(s3_path_prefix)
            conn.upload(s3_image_file_name, f, bucket=BUCKET_TARGET)
        print("Upload complete")
    finally:
        os.remove(image_file)

main()
