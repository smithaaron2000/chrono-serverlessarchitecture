#Imports Required
from threading import local
import boto3
from os.path import dirname
import time
#Specifying Region
AWS_REGION = "eu-west-1"

script_dir = dirname(__file__)

sess = boto3.Session(region_name=AWS_REGION)

cfnclient = sess.client('cloudformation')
s3 = sess.client('s3')
lambda_client = sess.client('lambda')
dynamoDB = sess.client('dynamodb')
sns = sess.client('sns')
iam = sess.client('iam')
athena = sess.client('athena')
sts = boto3.client("sts")

# response = cfnclient.describe_stack_resource(
#     StackName='ChronojumpStack',
#     LogicalResourceId='InputS3BucketForChronojumpDataFiles'
#     )

# resource = response['StackResourceDetail']
# bucket_name = resource['PhysicalResourceId']
# # print(bucket_name)

# get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
# objs = s3.list_objects_v2(Bucket=bucket_name)['Contents']
# last_added = [obj for obj in sorted(objs, key=get_last_modified)]
# print(last_added[-1]['Key'])

response = cfnclient.describe_stack_resource(
    StackName='ChronojumpStack',
    LogicalResourceId='InputS3BucketForChronojumpDataFiles'
)

resource = response['StackResourceDetail']
bucket_name = resource['PhysicalResourceId']

get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
objs = s3.list_objects_v2(Bucket=bucket_name)['Contents']
last_added = [obj for obj in sorted(objs, key=get_last_modified)]
name = last_added[-1]['Key']

localFilename = '/tmp/' + name
# for obj in objs:
#     name = str(obj['Key'])
#     print(name)

# localFilename = '/tmp/' + name

import glob
import os
home = os.path.expanduser("~")
direct = home + '/Desktop/ChronojumpCSVs/'
list_of_files = glob.glob(f'{direct}*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
#print(latest_file)