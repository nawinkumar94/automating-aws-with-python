import boto3
import click
from botocore.exceptions import ClientError
from pathlib import Path
import mimetypes

session = boto3.Session(profile_name='pythonAutomation')
s3 = session.resource('s3')

@click.group()
def cli():
    "Grop all the click commands"
    pass

@cli.command('list-buckets')
def list_buckets():
    "List all the buckets in S3"
    for bucket in s3.buckets.all():
         print(bucket)

@cli.command('list-buckets-objects')
@click.argument('bucket_name')
def list_buckets_objects(bucket_name):
    "List all the objects in S3 buckets"
    for object in s3.Bucket(bucket_name).objects.all():
         print(object)

@cli.command('setup-bucket')
@click.argument('bucket_name')
def setup_bucket(bucket_name):
    "Setup bucket for hosting a website also added the bucket policy"
    s3_bucket=None
    try:
        s3_bucket = s3.create_bucket(Bucket=bucket_name,
                                 CreateBucketConfiguration={'LocationConstraint': session.region_name})
    except ClientError as e:
        if e.response['Error']['Code']=='BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket_name)
        else:
            raise e

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
    policy=policy.strip();
    pol=s3.BucketPolicy(bucket_name)
    pol.put(Policy=policy)
    bucket_website = s3.BucketWebsite(bucket_name)
    bucket_website.put(WebsiteConfiguration={
        'ErrorDocument': {
            'Key': 'error.html'
        },
        'IndexDocument': {
            'Suffix': 'index.html'
        }
    })
    return
def upload_file(s3_bucket,path,key):
    content_type= mimetypes.guess_type(key)[0] or 'text/html'
    s3_bucket.upload_file(
        path,
        key,
        ExtraArgs={
            'ContentType':content_type
        })


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket_name')
def sync(pathname , bucket_name):
    "Sync the contents of the path name to bucket"
    root=Path(pathname).expanduser().resolve()
    s3_bucket = s3.Bucket(bucket_name)
    def handle_directory(target):
        for p in target.iterdir():
            if p.is_dir(): handle_directory(p)
            if p.is_file(): upload_file(s3_bucket,str(p.as_posix()),str(p.relative_to(root).as_posix()))

    handle_directory(root)

if __name__ == '__main__':
    cli()
