# -*- coding: utf-8 -*-
"""Class for s3 bucket."""
from pathlib import Path
from botocore.exceptions import ClientError
import mimetypes


class BucketManager:
    """Manage an S3 Bucket."""
    
    def __init__(self, session):
        """Create an BucketManager object."""
        self.session = session
        self.s3 = self.session.resource('s3')

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

    @staticmethod
    def upload_file(bucket, path, key):
        """Upload the file in to s3 bucket with path and key."""
        content_type = mimetypes.guess_type(key)[0] or 'text/html'
        return bucket.upload_file(
            path,
            key,
            ExtraArgs={
                'ContentType': content_type
            })

    def sync_bucket(self, pathname, bucket_name):
        """Sync the contents of the path name to bucket."""
        root = Path(pathname).expanduser().resolve()
        bucket = self.s3.Bucket(bucket_name)

        def handle_directory(target):
            for path_value in target.iterdir():
                if path_value.is_dir():
                    handle_directory(path_value)
                if path_value.is_file():
                    self.upload_file(bucket,
                                str(path_value.as_posix()),
                                str(path_value.relative_to(root).as_posix()))

        handle_directory(root)
