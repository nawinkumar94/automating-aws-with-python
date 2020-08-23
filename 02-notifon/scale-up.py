# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
scaling_client = session.client('autoscaling')

scaling_client.execute_policy(AutoScalingGroupName='Notifon Example Group', PolicyName='Scale Up')
