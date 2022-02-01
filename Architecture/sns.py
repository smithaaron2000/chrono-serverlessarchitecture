#Imports Required
import boto3
from os.path import dirname

#Specifying Region
AWS_REGION = "eu-west-1"

script_dir = dirname(__file__)

sess = boto3.Session(region_name=AWS_REGION)
sns = sess.client('sns')

topic = sns.create_topic(Name="ChronojumpDataUploadedSNSTopic")
topic_arn = topic["TopicArn"]

#Create Email Subscription
subsribe = sns.subscribe(TopicArn=topic_arn, Protocol="email", Endpoint="smithaaron2000@gmail.com", ReturnSubscriptionArn=True)
subscription_arn = subsribe["SubscriptionArn"]