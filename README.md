# automating-aws-with-python
Automating the AWS with python

# 01-Webotron
 Webotron is a script that will sync local directory with s3 bucket and optionally configure CloudFront and Route53 as well

 # Features
 Now Webotron has the following Features


#'pythonAutomation' configured profile name during aws configure
 -- List all the buckets in S3 "list_buckets()"
         "pipenv run python webotron\webotron.py --profile=pythonAutomation list-buckets"

 --List all the objects in S3 buckets "list_buckets_objects(bucket_name)"
         "pipenv run python webotron\webotron.py --profile=pythonAutomation list-buckets-objects 'bucket_name'"

 -- Create a new bucket and add public access policy and host the bucket for static website "setup_bucket(bucket_name)"
         "pipenv run python webotron/webotron.py --profile=pythonAutomation setup-bucket 'bucket_name'"

 --Sync a bucket with a path and key and upload files used pathlib and mimetypes  "sync(pathname , bucket_name)"
         "pipenv run python webotron/webotron.py --profile=pythonAutomation sync 'path' 'bucket'"

 --Added "get_bucket_url" method to load the bucket url when created and hosted a bucket

 --Method "load_manifest" gets E-tag for bucket in s3
   Method "generate_etag" generate the E-tag for Uploading file
   if both E-tag matches file is not uploaded again, if not we will upload the file.


  --- Tools for refactoring code
          "pipenv install -d pycodestyle"
          "pipenv install -d pydocstyle"
          "pipenv install -d pylint"
          "pipenv install -d pyflakes"
