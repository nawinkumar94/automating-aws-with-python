import boto3
import urllib

def start_label_detection(bucket_name, key):
    client = boto3.client('rekognition')
    response = client.start_label_detection(
        Video={'S3Object':
                {'Bucket':bucket_name,
                 'Name':key}
            })
    print(response)
    return


def start_processing_video(event, context):
    for record in event['Records']:
        start_label_detection(
                record['s3']['bucket']['name'],
                urllib.parse.unquote_plus(record['s3']['object']['key'])
        )

    return
