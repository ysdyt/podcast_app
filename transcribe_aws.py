import time
import boto3
import datetime
import re
import requests
import json
import pickle
import urllib
import sys
import os

dt_now = datetime.datetime.now()
dt_now_f = dt_now.strftime("%Y%m%d-%H%M%S")

args = sys.argv
file_name = args[1]
file_b_name = os.path.splitext(args[1])[0]

transcribe = boto3.client('transcribe')
job_name = dt_now_f
job_uri = "https://s3-ap-northeast-1.amazonaws.com/ysdyt-audios/{}".format(file_name)
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',
    LanguageCode='ja-JP'
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
print(status)

# Save the transcribed result =================

full_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']

uri = re.search('https.+\.json', full_uri).group()
amz_stoken = re.search('X-Amz-Security-Token=(.+)&X-Amz-Algorithm', full_uri).group(1)
amz_al = re.search('X-Amz-Algorithm=(.+)&X-Amz-Date', full_uri).group(1)
amz_date = re.search('X-Amz-Date=(.+)&X-Amz-SignedHeaders', full_uri).group(1)
amz_header = re.search('X-Amz-SignedHeaders=(.+)&X-Amz-Expires', full_uri).group(1)
amz_expire = re.search('X-Amz-Expires=(.+)&X-Amz-Credential', full_uri).group(1)
amz_creden = re.search('X-Amz-Credential=(.+)&X-Amz-Signature', full_uri).group(1)
amz_sign = re.search('X-Amz-Signature=(.+)', full_uri).group(1)

#print(uri)
#print(amz_stoken)
#print(urllib.parse.unquote(amz_stoken))
#print(amz_al)
#print(amz_date)
#print(amz_header)
#print(amz_expire)
#print(amz_creden)
#print(urllib.parse.unquote(amz_creden))
#print(amz_sign)

params = (
    ('X-Amz-Security-Token', urllib.parse.unquote(amz_stoken)), #decode
    ('X-Amz-Algorithm', amz_al),
    ('X-Amz-Date', amz_date),
    ('X-Amz-SignedHeaders', amz_header),
    ('X-Amz-Expires', amz_expire),
    ('X-Amz-Credential', urllib.parse.unquote(amz_creden)), #decode
    ('X-Amz-Signature', amz_sign),
)

response = requests.get(uri, params=params)
#print(response)
transcribed_result = response.json()
#print(transcribed_result)

new_dir_path = './transcribed_file'
os.makedirs(new_dir_path, exist_ok=True)
with open('./transcribed_file/{}.pickle'.format(file_b_name), 'wb') as f:
    pickle.dump(transcribed_result, f)
