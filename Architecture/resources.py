#Imports Required
import boto3
from os.path import dirname

#Specifying Region
AWS_REGION = "eu-west-1"

script_dir = dirname(__file__)

sess = boto3.Session(region_name=AWS_REGION)

cfnclient = sess.client('cloudformation')


stack = cfnclient.describe_stacks(StackName='ChronojumpStack')

stack_status = stack['Stacks'][0]['StackStatus']

print(stack_status)