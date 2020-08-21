#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Webotron Deploy the websites with AWS.

Webotron automates the process of deploying the static website hosting
- Configure AWS S3 buckets
    -Create them
    -Set them for static website hosting
    -Deploy the local files in to them
- Configure DNS with AWS Route53
- Configure the Content Delivery Network and SSL with AWS.
"""

import boto3
import click
from bucket import BucketManager


session = None
bucket_manager = None


@click.group()
@click.option('--profile', default=None, help= "Add profile for the credentials" )
def cli(profile):
    """Grop all the click commands."""
    global session, bucket_manager
    session_data={}
    if profile:
        session_data['profile_name']=profile
    session = boto3.Session(**session_data)
    bucket_manager = BucketManager(session)


@cli.command('list-buckets')
def list_buckets():
    """List all the buckets in S3."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-buckets-objects')
@click.argument('bucket_name')
def list_buckets_objects(bucket_name):
    """List all the objects in S3 buckets."""
    for object in bucket_manager.all_objects(bucket_name):
        print(object)


@cli.command('setup-bucket')
@click.argument('bucket_name')
def setup_bucket(bucket_name):
    """Set up bucket for hosting a website also added the bucket policy."""
    s3_bucket = bucket_manager.init_bucket(bucket_name)
    bucket_manager.set_bucket_policy(bucket_name)
    bucket_manager.bucket_website(bucket_name)


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket_name')
def sync(pathname, bucket_name):
    """Sync the contents of the path name to bucket."""
    bucket_manager.sync_bucket(pathname, bucket_name)


if __name__ == '__main__':
    cli()
