# coding: utf-8
event = {'Records': [{'EventSource': 'aws:sns', 'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:us-east-1:884362627737:handleLableDetectionTopic:b0140238-ab3a-44eb-bd7b-687255c63d86', 'Sns': {'Type': 'Notification', 'MessageId': 'e94f9317-6a56-5f70-b611-c4a9d00e2fb0', 'TopicArn': 'arn:aws:sns:us-east-1:884362627737:handleLableDetectionTopic', 'Subject': None, 'Message': '{"JobId":"1930768dd86e02def7f842833cc8f53c53b6e2112d29406858e057d6431cf6b2","Status":"SUCCEEDED","API":"StartLabelDetection","Timestamp":1598339096778,"Video":{"S3ObjectName":"Pexels Videos 2670.mp4","S3Bucket":"video-analyze-nk-01"}}', 'Timestamp': '2020-08-25T07:04:56.857Z', 'SignatureVersion': '1', 'Signature': 'FrAL/ZrCBY6Ri4Bi2dN9ffrJ7sovC6PJO8WcmR6wcngA/JnOLeNTFKmuSmP8h3y86urKr9QlgmfeR02j/KJEojHrhl181ihOSMJOFWoBdF0IG19H1uitXs6dr5FaMD+U0UHMTB1tOLlnrrB5lZYwYhJf8sAEBWdUnouvPP97i2pkhcqL7BzRiTeb0tX31xGF3xR0/b1gA6e1YIB+YDPxS8Vezba2r+v0QOtdqBenkEHf0hlxldoSuKOSMArzbYgn1zv6lkii93k90uY/g1xh2DSzCuRawCy8TprJFeB7Qu+NRCNlTAl5ruTfcR3xSvCVVd8OjuJ1CbLfgTy9PPAFIg==', 'SigningCertUrl': 'https://sns.us-east-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem', 'UnsubscribeUrl': 'https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:884362627737:handleLableDetectionTopic:b0140238-ab3a-44eb-bd7b-687255c63d86', 'MessageAttributes': {}}}]}
event
event['Records'][0]
event['Records'][0]['EventSubscriptionArn']
event['Records'][0]['Sns']
event['Records'][0]['Sns']['Message']
event['Records'][0]['Sns']['Message']['jobId']
import json
type(event['Records'][0]['Sns']['Message']['jobId'])
type(event['Records'][0]['Sns']['Message'])
event['Records'][0]['Sns']['Message']
json.loads(event['Records'][0]['Sns']['Message'])
data=json.loads(event['Records'][0]['Sns']['Message'])
data['JobId']
