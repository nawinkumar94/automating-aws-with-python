import boto3
import click

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

if __name__ == '__main__':
    cli()
