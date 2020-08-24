# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
s3=session.resource('s3')
path_name = '~/Downloads/Pexels Videos 1674470.mp4'

from pathlib import Path
path=Path(path_name).expanduser().resolve()
path
bucket
bucket=s3.Bucket('video-analyze-nk')
s3.Bucket(bucket.name).upload_file(str(path.as_posix()),str(path.name))
client = session.client('rekognition')

response = client.start_label_detection(
    Video={'S3Object': {'Bucket':bucket.name, 'Name':path.name}})
response
job_id = response['JobId']

response = client.get_label_detection(
    JobId=job_id)

response['JobStatus']

response['Labels']
len(response['Labels'])
