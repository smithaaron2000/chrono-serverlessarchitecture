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

processor_function = lambda_client.create_function(FunctionName="ChronojumpProcessor", Runtime="python3.9", 
                                                   Handler="ChronojumpProcessor.lambda_handler",
                                                   Role="arn:aws:iam::846950971618:role/ChronojumpProcessorRole",
                                                   Code={'ZipFile': open(f"{script_dir}ChronojumpProcessor.zip", 'rb').read()}, Timeout = 120)


# get_processor_function = lambda_client.get_function_configuration(FunctionName="ChronojumpDataProcessor")
# function_arn = get_processor_function['FunctionArn']

# permission = lambda_client.add_permission(
#     FunctionName='ChronojumpDataProcessor',
#     StatementId='S3BucketPermission',
#     Action='lambda:InvokeFunction',
#     Principal='s3.amazonaws.com',)

# policy = lambda_client.get_policy(FunctionName='ChronojumpDataProcessor')

# bucket_name = "chronojumpstack-inputs3bucketforchronojumpdatafil-u2a74f6x7eim"

# trigger = s3.put_bucket_notification_configuration(Bucket=bucket_name,
#         NotificationConfiguration={
#         'LambdaFunctionConfigurations': [
#             {
#                 'LambdaFunctionArn': function_arn,
#                 'Events': [
#                     's3:ObjectCreated:*'
#                 ],
#             },
#         ]})