# coding: utf-8
import boto3
session = boto3.Session(profile_name='pythonAutomation')
ec2 = session.resource('ec2')
key_path = key_name + '.pem'
key_path
key_pair = ec2.create_key_pair(KeyName=key_name)
key_pair
key_pair.key_material
with open(key_path, 'w') as key_file:
    key_file.write(key_pair.key_material)

import os,stat
os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
#This allow only the root user to read and write the file
ec2.images.filter(Owners=['amazon'])
len(list(ec2.images.filter(Owners=['amazon'])))
image = ec2.Image('ami-0a780d5bac870126a')
image.name
ami_name = 'amzn-ami-hvm-2018.03.0.20200729.0-x86_64-gp2'
ami_name
filters = [{'Name' : 'name' , 'Values' : [ami_name]}]
list(ec2.images.filter(Owners=['amazon'],Filters = filters))
image
instance = ec2.create_instances(ImageId=image.id,InstanceType='t2.micro',KeyName=key_pair.key_name ,MaxCount=1 ,MinCount=1)
instance
key_pair
key_pair.name
key_pair.key_name
list(key_pair)
instance
instance[0]
inst = instance[0]
inst.terminate()
instance = ec2.create_instances(ImageId=image.id,InstanceType='t2.micro',KeyName=key_pair.key_name ,MaxCount=1 ,MinCount=1)
inst = instance[0]
inst
inst.public_dns_name
inst.wait_until_running()
inst.reload()
inst.public_dns_name
inst.security_groups
inst.security_groups[0]['GroupId']
inst.security_group
inst.security_groups
security_group = inst.security_groups[0]['GroupId']
security_group = ec2.SecurityGroup(inst.security_groups[0]['GroupId'])
security_group.authorize_ingress(IpPermissions=[{'FromPort': 22, 'ToPort': 22, 'IpProtocol':'TCP', 'IpRanges': [{'CidrIp': '192.168.43.102/32'}]}])
security_group.authorize_ingress(IpPermissions=[{'FromPort': 80, 'ToPort': 80, 'IpProtocol':'TCP', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}])
inst.public_dns_name
