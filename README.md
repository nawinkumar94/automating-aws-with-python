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


--- Use command python -m webotron.webotron


# 02-Notifon
  Notifon is a project that allows the slack users to get notifications on changes in aws using cloud watch events

#Features
  Notifon has the following features
    ---> Send notification to slack using serverless. when the cloud watch events happens by
         auto scaling groups or lambda functions.

#Commands for serverless application

  # create a serverless application
    --> serverless create --template aws-python3 --name notifon-notifier
    --> serverless create -t "Name of template" -n "Name of the lamba function"
  # To deploy application
    --> sls deploy
  # Invoke a function('startProcessingVideo'-->name of function)
    --> sls invoke -f startProcessingVideo
  # To check logs('startProcessingVideo'-->name of function)
    --> sls logs -f startProcessingVideo -t

# 03-video-analyzer
  When the video file is uploaded in to s3,gets the info about the video using 'rekognition' by 'start_label_detection' function.
  Triggers the SNS event when video is uploaded in to S3 and start the lambda function , upload the collected informations in DynamoDB table

  # Command to add video in to s3 bucket using pathlib "upload_files(profile, path_name, bucket_name)"
    ---> pipenv run python upload-file.py --profile=pythonAutomation  "~/Downloads/Pexels Videos 2670.mp4" video-analyze-nk-01
