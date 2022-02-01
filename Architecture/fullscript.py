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

###### Creating Cloud Formation Stack #########

stack = ''
with open(f"{script_dir}stack.json", 'r') as fd:
    stack = fd.read()


capabilities=[
        'CAPABILITY_IAM',
        'CAPABILITY_NAMED_IAM',
    ]

cfnclient.create_stack(StackName='ChronojumpStack', TemplateBody=stack, Capabilities=capabilities)

print("Cloudformation Stack creating...")
print(".")
print(".")
print(".")

time.sleep(90)

stack = cfnclient.describe_stacks(StackName='ChronojumpStack')
stack_status = stack['Stacks'][0]['StackStatus']
print(stack_status)
print(".")
print(".")
print(".")

########## Creating SNS Topic ###########

topic = sns.create_topic(Name="ChronojumpDataUploadedSNSTopic")
topic_arn = topic["TopicArn"]

#Create Email Subscription
subsribe = sns.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint="smithaaron2000@gmail.com", ReturnSubscriptionArn=True)
subscription_arn = subsribe["SubscriptionArn"]

print("SNS Topic Created...")
print(".")
print(".")
print(".")

###### Creating Lambda function to process CSV file ######

processor_function = lambda_client.create_function(FunctionName="ChronojumpProcessor", Runtime="python3.9", 
                                                Handler="ChronojumpProcessor.lambda_handler",
                                                Role="arn:aws:iam::846950971618:role/ChronojumpProcessorRole",
                                                Code={'ZipFile': open(f"{script_dir}ChronojumpProcessor.zip", 'rb').read()}, Timeout = 120)


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

print("Data Processor function created...")
print(".")
print(".")
print(".")
time.sleep(3)

###### Creating trigger in S3 for Lambda function ######

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

########### Creating Lambda function to notify subscribers ###############

notifier_function = lambda_client.create_function(FunctionName="ChronojumpDataUploadNotifier", Runtime="python3.9", 
                                                Handler="ChronojumpDataUploadNotifier.lambda_handler",
                                                Role="arn:aws:iam::846950971618:role/ChronojumpDataUploadNotifierRole",
                                                Code={'ZipFile': open(f"{script_dir}ChronojumpDataUploadNotifier.zip", 'rb').read()})

get_function = lambda_client.get_function_configuration(FunctionName="ChronojumpDataUploadNotifier")
function_arn = get_function['FunctionArn']

response = lambda_client.add_permission(
    FunctionName='ChronojumpDataUploadNotifier',
    StatementId='DBTablePermission',
    Action='lambda:InvokeFunction',
    Principal='dynamodb.amazonaws.com',)

response2 = lambda_client.get_policy(FunctionName='ChronojumpDataUploadNotifier')


table = dynamoDB.describe_table(
    TableName='CMJ',
)

resource = table['Table']
stream_arn = resource['LatestStreamArn']

time.sleep(3)

print("Notifier function created...")
print(".")
print(".")
print(".")

########## Adding trigger in Lambda function for DynamoDB table ###########

trigger = lambda_client.create_event_source_mapping(
    EventSourceArn= stream_arn,
    FunctionName='ChronojumpDataUploadNotifier',
    Enabled=True,
    BatchSize=123,
    StartingPosition='TRIM_HORIZON',
)

print("Resources Created :)")

