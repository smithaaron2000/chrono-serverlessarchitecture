from datetime import datetime
import boto3
from os.path import dirname

#Specifying Region
AWS_REGION = "eu-west-1"

sess = boto3.Session(region_name=AWS_REGION)

s3 = boto3.resource('s3')
cfnclient = sess.client('cloudformation')

script_dir = dirname(__file__)

response = cfnclient.describe_stack_resource(
    StackName='ChronojumpStack',
    LogicalResourceId='InputS3BucketForChronojumpDataFiles'
)

resource = response['StackResourceDetail']
bucket_name = resource['PhysicalResourceId']

now = datetime.now() # current date and time
date_time = now.strftime("%d-%m-%Y")
object_name = 'session' + date_time + '.csv'

#s3.meta.client.upload_file(f"{script_dir}session.csv", bucket_name, 'session.csv')
s3.meta.client.upload_file("/home/aaron/Desktop/ChronojumpCSVs/session.csv", bucket_name, object_name)
