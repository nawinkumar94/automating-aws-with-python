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
import util
from bucket import BucketManager
from domain import DomainManager


session = None
bucket_manager = None
domain_manager = None


@click.group()
@click.option('--profile', default=None,
                help= "Add profile for the credentials")
def cli(profile):
    """Grop all the click commands."""
    global session, bucket_manager, domain_manager
    session_data = {}
    if profile:
        session_data['profile_name'] = profile
    session = boto3.Session(**session_data)
    bucket_manager = BucketManager(session)
    domain_manager = DomainManager(session)


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
    print("The URL of hosted bucket is : "
                    +bucket_manager.get_bucket_url(bucket_name))


@cli.command('setup-domain')
@click.argument('domain_name')
def setup_domain(domain_name):
    """Set the domain name for the bucket."""
    # since both bucket and domain should be a same,setting bucket name to domain_name
    bucket_name = domain_name
    zone =  domain_manager.find_hosted_zone(domain_name) \
            or domain_manager.create_hosted_zone(domain_name)
    endpoint = util.region_endpoint(bucket_manager.get_region_name(bucket_name))
    domain_manager.create_s3_domain_record(zone, domain_name, endpoint)

if __name__ == '__main__':
    cli()
