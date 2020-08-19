# automating-aws-with-python
Automating the AWS with python

# 01-Webotron
 Webotron is a script that will sync local directory with s3 bucket and optionally configure CloudFront and Route53 as well

 # Features
 Now Webotron has the following Features

 -- List all the buckets in S3 "list_buckets()"
         "pipenv run python webotron\webotron.py list-buckets"

 --List all the objects in S3 buckets "list_buckets_objects(bucket_name)"
         "pipenv run python webotron\webotron.py list-buckets-objects 'bucket_name'"

 -- Create a new bucket and add public access policy and host the bucket for static website "setup_bucket(bucket_name)"
         "pipenv run python webotron/webotron.py setup-bucket 'bucket_name'"

 --Sync a bucket with a path and key and upload files used pathlib and mimetypes  "sync(pathname , bucket_name)"
         "pipenv run python webotron/webotron.py sync 'path' 'bucket'"
