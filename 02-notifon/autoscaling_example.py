# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
scaling_client = session.client('autoscaling')
scaling_client
scaling_client.describe_policies(AutoScalingGroupName='Notifon Example Group', PolicyNames=['Scale Up'])
scaling_client.execute_policy(AutoScalingGroupName='Notifon Example Group', PolicyNames='Scale Up')
scaling_client.execute_policy(AutoScalingGroupName='Notifon Example Group', PolicyName='Scale Up')
scaling_client.execute_policy(AutoScalingGroupName='Notifon Example Group', PolicyName='Scale Up')
