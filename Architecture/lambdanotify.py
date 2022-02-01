#Imports Required
import boto3
from os.path import dirname

#Specifying Region
AWS_REGION = "eu-west-1"

script_dir = dirname(__file__)

sess = boto3.Session(region_name=AWS_REGION)

lambda_client = sess.client('lambda')
cfnclient = sess.client('cloudformation')
dynamoDB = sess.client('dynamodb')


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


trigger = lambda_client.create_event_source_mapping(
    EventSourceArn= stream_arn,
    FunctionName='ChronojumpDataUploadNotifier',
    Enabled=True,
    BatchSize=123,
    StartingPosition='TRIM_HORIZON',
)