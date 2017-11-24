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
from time import sleep
from PIL import Image
from resizeimage import resizeimage
import datetime

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
    camera.exposure_mode = "night"
    # warm up the camera before you use it!
    sleep(5)

    image_file = config[cam_upload_config_key]['TempFileName']
    small_image_file = "small{}".format(image_file)
    s3_path_prefix = config[cam_upload_config_key]['S3PathPrefix']
    days_to_expire = timedelta(days=int(config[cam_upload_config_key]['DaysToExpire']))

    try:
        print("Capturing image")
        try:
            camera.capture(image_file)
        finally:
            camera.close()
        print("Captured, now uploading")

        with open(image_file, 'r+b') as image_file_handle:
            with Image.open(image_file_handle) as image:
                image = image.convert("RGB")
                cover = resizeimage.resize_contain(image, [480, 480])
                cover = cover.convert("RGB")
                cover.save(small_image_file, image.format)

        epoch_time = int(time.time())
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

        with open (image_file, "rb") as f:
            s3_image_file_name = '{}{:d}cam.jpg'.format(s3_path_prefix, epoch_time)
            conn.upload(s3_image_file_name, f, bucket=BUCKET_TARGET, expires=days_to_expire)

        with open (small_image_file, "rb") as f:
            s3_small_image_file_name = '{}{:d}smallcam.jpg'.format(s3_path_prefix, epoch_time)
            conn.upload(s3_small_image_file_name, f, bucket=BUCKET_TARGET, expires=days_to_expire)

        update_log({"image":s3_image_file_name, "previewImage" : s3_small_image_file_name, "timestamp": timestamp})

        with open (RECENT_LOG, "rb") as f:
            s3_log = '{}log.json'.format(s3_path_prefix)
            conn.upload(s3_log, f, bucket=BUCKET_TARGET)
        print("Upload complete")
    finally:
        os.remove(image_file)

main()
