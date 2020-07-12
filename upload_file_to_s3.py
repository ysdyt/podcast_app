#! /usr/bin/python

import os
import sys
import boto3

args = sys.argv
src_path = args[1]
src_fname = os.path.basename(src_path)
bucket_name = "ysdyt-audios" #change it into your S3bucket name

s3 = boto3.resource('s3')
s3.Bucket(bucket_name).upload_file(src_path, src_fname)
print('finished cp the file to s3-bucket')

# show exists files in the bucket
for object in s3.Bucket(bucket_name).objects.all():
    print(object.key)
