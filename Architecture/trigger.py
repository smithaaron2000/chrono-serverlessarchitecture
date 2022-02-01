#Imports Required
import boto3
import uuid
from os.path import dirname

#Specifying Region
AWS_REGION = "eu-west-1"

script_dir = dirname(__file__)

sess = boto3.Session(region_name=AWS_REGION)

s3 = sess.client('s3')
lambda_client = sess.client('lambda')
cfnclient = sess.client('cloudformation')

get_processor_function = lambda_client.get_function_configuration(FunctionName="ChronojumpProcessor")
function_arn = get_processor_function['FunctionArn']

permission = lambda_client.add_permission(
    FunctionName='ChronojumpProcessor',
    StatementId='S3BucketPermission',
    Action='lambda:InvokeFunction',
    Principal='s3.amazonaws.com',)

policy = lambda_client.get_policy(FunctionName='ChronojumpProcessor')

response = cfnclient.describe_stack_resource(
    StackName='ChronojumpStack',
    LogicalResourceId='InputS3BucketForChronojumpDataFiles'
)

resource = response['StackResourceDetail']
bucket_name = resource['PhysicalResourceId']

trigger = s3.put_bucket_notification_configuration(Bucket=bucket_name,
        NotificationConfiguration={
        'LambdaFunctionConfigurations': [
            {
                'LambdaFunctionArn': function_arn,
                'Events': [
                    's3:ObjectCreated:*'
                ],
            },
        ]})