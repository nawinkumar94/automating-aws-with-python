import os
import json
import boto3
import urllib

#Helper functions
def start_label_detection(bucket_name, key):
    """start detection of labels in a stored video and returns the JodId of rekognition."""
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.start_label_detection(
        Video={'S3Object':
                {'Bucket':bucket_name,
                 'Name':key}
            },
        NotificationChannel={
            'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
            'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
            })
    return

def get_lable_detection(job_id):
    """Gets the label detection results of video with job_id of start_label_detection."""
    rekognition_client = boto3.client('rekognition')
    response = rekognition_client.get_label_detection(JobId = job_id)
    next_token = response.get('NextToken', None)

    while next_token:
        next_page = rekognition_client.get_label_detection(
                            JobId = job_id,
                            NextToken = next_token)

        next_token = next_page.get('NextToken', None)
        response['Labels'].extend(next_page['Lables'])

    return response

def make_item(data):
    """Process the float items in list and dict to string."""
    if isinstance(data, dict):
        return { k: make_item(v) for k, v in data.items() }
    if isinstance(data,list):
        return [ make_item(v) for v in data ]
    if isinstance(data,float):
        return str(data)

    return data

def put_lable_in_dynamodb(data,video_bucket_name, video_object_name):
    """Inserts the data in dynamodb table."""
    del data['ResponseMetadata']
    del data['JobStatus']
    data['Video_Bucket'] = video_bucket_name
    data['Video_Name'] = video_object_name
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['VIDEO_ANALYZER_TABLE']
    video_table = dynamodb.Table(table_name)
    data = make_item(data)
    video_table.put_item(Item=data)
    return

# Lambda functions
def start_processing_video(event, context):
    """When the video is uploaded in to s3 it triggers start_processing_video."""
    for record in event['Records']:
        start_label_detection(
                record['s3']['bucket']['name'],
                urllib.parse.unquote_plus(record['s3']['object']['key'])
        )

    return

def handle_lable_detection(event, context):
    """This function gets ths data in SNS to upload the data in dynamodb."""
    for records in event['Records']:
        # 'json.loads' converts the string value to json if the string is in JSON format
        message = json.loads(records['Sns']['Message'])
        job_id = message['JobId']
        video_object_name = message['Video']['S3ObjectName']
        video_bucket_name = message['Video']['S3Bucket']
        response = get_lable_detection(job_id)
        put_lable_in_dynamodb(response, video_bucket_name, video_object_name)
