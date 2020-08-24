# coding: utf-8
event = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1', 'eventTime': '2020-08-24T13:44:47.487Z', 'eventName': 'ObjectCreated:Put', 'userIdentity': {'principalId': 'AWS:AIDA432A6ZKM2LJFACSZZ'}, 'requestParameters': {'sourceIPAddress': '157.49.212.222'}, 'responseElements': {'x-amz-request-id': '8ACC1A23E716C462', 'x-amz-id-2': 'RgzSm4objTVCwqM8fslTbfBLZ6Z8KHMqoFOQFt474Kq831D599xxoXTefk9NvE0KOCZrnvRyFVIr3NiFZImvZLvQjgymVwnH'}, 's3': {'s3SchemaVersion': '1.0', 'configurationId': '30bbac26-cb9c-457b-ac11-32aa0295b795', 'bucket': {'name': 'video-analyze-nk-01', 'ownerIdentity': {'principalId': 'A353FYET5RPUK6'}, 'arn': 'arn:aws:s3:::video-analyze-nk-01'}, 'object': {'key': 'Pexels+Videos+2670.mp4', 'size': 7606633, 'eTag': '0574c053c8686c3f1dc0aa3743e45cb9', 'sequencer': '005F43C3CE1EB4E4B5'}}}]}
event
event['Records']
event['Records'][0]['s3']['bucket']
event['Records'][0]['s3']['bucket']['name']
event['Records'][0]['s3']['object']['key']

import urllib
urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
