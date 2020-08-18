# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print(bucket)

#creating bucket using boto3
#new_bucket=s3.create_bucket(Bucket='pythonautomation-nk-boto3',CreateBucketConfiguration={
#        'LocationConstraint':'ap-south-1'})
