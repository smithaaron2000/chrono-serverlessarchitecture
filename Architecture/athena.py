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
athena = sess.client('athena')
sts = boto3.client("sts")

## Creating Athena Workgroup

account_id = sts.get_caller_identity()["Account"]

response = cfnclient.describe_stack_resource(
    StackName='ChronojumpStack',
    LogicalResourceId='OutputS3BucketForAthenaData'
)

resource = response['StackResourceDetail']
bucket_name = resource['PhysicalResourceId']
s3_path = 's3://' + bucket_name + '/'
account_id = sts.get_caller_identity()["Account"]

versions = athena.list_engine_versions(
    MaxResults=10
)

workgroup = athena.create_work_group(
    Name='athenav2',
    Configuration={
        'ResultConfiguration': {
            'OutputLocation': s3_path,
            'EncryptionConfiguration': {
                'EncryptionOption': 'SSE_S3'
            }
        },
        'EnforceWorkGroupConfiguration': False,
        'PublishCloudWatchMetricsEnabled': True,
        'BytesScannedCutoffPerQuery': 10000000,
        'RequesterPaysEnabled': False,
        'EngineVersion': {
            'SelectedEngineVersion': 'Athena engine version 2',
            'EffectiveEngineVersion': 'Athena engine version 2'
        }
    }
)