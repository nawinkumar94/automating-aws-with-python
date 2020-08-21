# -*- coding: utf-8 -*-
"""Class for s3 bucket."""
from pathlib import Path
from functools import reduce
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
from hashlib import md5
import mimetypes
import util


class BucketManager:
    """Manage an S3 Bucket."""
    CHUNK_SIZE = 8388608

    def __init__(self, session):
        """Create an BucketManager object."""
        self.session = session
        self.s3 = self.session.resource('s3')
        self.transfer_config = TransferConfig(
            multipart_chunksize=self.CHUNK_SIZE,
            multipart_threshold=self.CHUNK_SIZE
        )
        self.manifest = {}

    def all_buckets(self):
        """Get an iterator all the buckets."""
        return self.s3.buckets.all()

    def all_objects(self, bucket_name):
        """Get an iterator all the objects in bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self, bucket_name):
        """Create a new bucket or return the name of the bucket if already exists."""
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': self.session.region_name})
        except ClientError as error:
            if error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise error
        return s3_bucket

    def set_bucket_policy(self, bucket_name):
        """Set bucket policy to the bucket."""
        policy = """
        {
            "Id": "Policy1597808344458",
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Stmt1597808341979",
                    "Action": [
                        "s3:GetObject"
                    ],
                    "Effect": "Allow",
                    "Resource": "arn:aws:s3:::%s/*",
                    "Principal": "*"
                }
            ]
        }
        """ % bucket_name
        policy = policy.strip()
        pol = self.s3.BucketPolicy(bucket_name)
        pol.put(Policy=policy)

    def bucket_website(self, bucket_name):
        """Add the files in the bucket to host a website."""
        bucket_website = self.s3.BucketWebsite(bucket_name)
        bucket_website.put(WebsiteConfiguration={
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        })

    def get_region_name(self,bucket_name):
        """Getting the location of the bucket."""
        client = self.s3.meta.client
        bucket_location=client.get_bucket_location(Bucket=bucket_name)
        return bucket_location["LocationConstraint"] or 'us-east-1'

    def get_bucket_url(self,bucket_name):
        """Getting the URL of the bucket fro which the static website is hosted."""
        if util.known_region(self.get_region_name(bucket_name)):
            bucket_url="http://{}.{}".format(bucket_name,util.region_endpoint(self.get_region_name(bucket_name)).host)
            return bucket_url
        else:
            return "invalid URL"

    def load_manifest(self,bucket_name):
        """Load the Etag for the files in the bucket to compare with Etag of uploading file."""
        paginator=self.s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket= bucket_name):
            for obj in page.get('Contents',[]):
                self.manifest[obj['Key']]=obj['ETag']


    @staticmethod
    def hash_data(data):
        """Generate hash in md5 format for the data."""
        hash = md5()
        hash.update(data)
        return hash;

    def generate_etag(self, path):
        """Generate Etag for the uploading files based on the CHUNK size
            and compare with of files in bucket."""
        hashes = []
        with open(path, 'rb') as file:
            while True:
                #Read the data upto the chunk size.
                data =  file.read(self.CHUNK_SIZE)
                # Loop becomes fales if teh data size is more than chunck size.
                if not data:
                    break

                hashes.append(self.hash_data(data))

        if not hashes:
            return
        elif len(hashes) == 1:
            return '"{}"'.format(hashes[0].hexdigest())
        else:
            # If the file size is greater than chunk size AWS uses multipart upload api,
            # append all the tag with size of the file.
            hash = self.hash_data(reduce(lambda x, y: x + y, (h.digest() for h in hashes)))
            return '"{}-{}"'.format(hash.hexdigest(), len(hashes))


    def upload_file(self, bucket, path, key):
        """Upload the file in to s3 bucket with path and key."""
        content_type = mimetypes.guess_type(key)[0] or 'text/html'
        etag_upload_file = self.generate_etag(path)
        print('etag_upload_file  {} '.format(etag_upload_file))
        print('self.manifest.get(key)  {} '.format(self.manifest.get(key)))
        if self.manifest.get(key, '') == etag_upload_file:
            print("Skipping already uploaded key {} :".format(etag_upload_file))
            return

        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            },
            Config=self.transfer_config
            )


    def sync_bucket(self, pathname, bucket_name):
        """Sync the contents of the path name to bucket."""
        root = Path(pathname).expanduser().resolve()
        bucket = self.s3.Bucket(bucket_name)
        self.load_manifest(bucket_name)
        def handle_directory(target):
            for path_value in target.iterdir():
                if path_value.is_dir():
                    handle_directory(path_value)
                if path_value.is_file():
                    self.upload_file(bucket,
                                str(path_value.as_posix()),
                                str(path_value.relative_to(root).as_posix()))

        handle_directory(root)
