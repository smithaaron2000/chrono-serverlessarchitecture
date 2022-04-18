from datetime import datetime
import boto3
import glob
import os
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

home = os.path.expanduser("~")
direct = home + '/Desktop/ChronojumpCSVs/'
list_of_files = glob.glob(f'{direct}*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

s3.meta.client.upload_file(latest_file, bucket_name, object_name)    
