#!/usr/bin/python

import boto3
import click
from pathlib import Path

@click.command('upload-files')
@click.option('--profile', default=None, help= "Enter the profile configured during aws authorize")
@click.argument('path_name')
@click.argument('bucket_name')
def upload_files(profile, path_name, bucket_name):
    session_data = {}
    if profile:
        session_data['profile_name'] = profile
    session = boto3.Session(**session_data)
    s3 = session.resource('s3')

    path = Path(path_name).expanduser().resolve()
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file((path.as_posix()),str(path.name))

if __name__ == '__main__':
    upload_files()
