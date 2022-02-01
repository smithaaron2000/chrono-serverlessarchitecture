#Imports Required
import boto3
from os.path import dirname

#Specifying Region
AWS_REGION = "eu-west-1"

script_dir = dirname(__file__)

sess = boto3.Session(region_name=AWS_REGION)

cfnclient = sess.client('cloudformation')

###### Creating Cloud Formation Stack #########

stack = ''
with open(f"{script_dir}stack.json", 'r') as fd:
    stack = fd.read()


capabilities=[
        'CAPABILITY_IAM',
        'CAPABILITY_NAMED_IAM',
    ]

cfnclient.create_stack(StackName='ChronojumpStack', TemplateBody=stack, Capabilities=capabilities)

stack = cfnclient.describe_stacks(StackName='ChronojumpStack')

stack_status = stack['Stacks'][0]['StackStatus']

print(stack_status)