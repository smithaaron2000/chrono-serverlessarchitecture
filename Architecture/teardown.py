#Imports Required
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
athena=sess.client('athena')
s3resource = boto3.resource('s3')


input_bucket = cfnclient.describe_stack_resource(
    StackName='ChronojumpStack',
    LogicalResourceId='InputS3BucketForChronojumpDataFiles'
)

input_resource = input_bucket['StackResourceDetail']
input_bucket_name = input_resource['PhysicalResourceId']
i_bucket = s3resource.Bucket(input_bucket_name)
i_bucket.objects.all().delete()

output_bucket = cfnclient.describe_stack_resource(
    StackName='ChronojumpStack',
    LogicalResourceId='OutputS3BucketForAthenaData'
)

output_resource = output_bucket['StackResourceDetail']
output_bucket_name = output_resource['PhysicalResourceId']
o_bucket = s3resource.Bucket(output_bucket_name)
o_bucket.objects.all().delete()

delete = cfnclient.delete_stack(
    StackName='ChronojumpStack',
)

response = lambda_client.delete_function(
    FunctionName='ChronojumpProcessor',
)

response = lambda_client.delete_function(
    FunctionName='ChronojumpDataUploadNotifier',
)

response = athena.delete_work_group(
    WorkGroup='athenav2',
    RecursiveDeleteOption=True

)