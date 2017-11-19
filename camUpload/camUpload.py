import picamera
import tinys3
import configparser
import time

config = configparser.ConfigParser()
config.read('camUpload.ini')
S3_ACCESS_KEY = config['aws']['AccessID']
S3_SECRET_KEY = config['aws']['SecretKey']
BUCKET_TARGET = config['aws']['BucketTarget']
conn = tinys3.Connection(S3_ACCESS_KEY,S3_SECRET_KEY,tls=True)

camera = picamera.PiCamera()
image_file = config['camupload']['TempFileName']
camera.capture(image_file)

epoch_time = int(time.time())

f = open(image_file,'rb')
conn.upload('{:d}cam.jpg'.format(epoch_time),f, bucket=BUCKET_TARGET)
