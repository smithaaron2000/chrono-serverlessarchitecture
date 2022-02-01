# ChronojumpUploadDataNotifier Lambda function
#
# This function is triggered when values are inserted into the CMJ DynamoDB table.

from __future__ import print_function
import json, boto3

# Connect to SNS
sns = boto3.client('sns')
alertTopic = 'ChronojumpDataUploadedSNSTopic'
snsTopicArn = [t['TopicArn'] for t in sns.list_topics()['Topics'] if t['TopicArn'].lower().endswith(':' + alertTopic.lower())][0]
print(snsTopicArn)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
countermovementTableName = 'CMJ'
countermovementTable = dynamodb.Table(countermovementTableName);

# This handler is executed every time the Lambda function is triggered
def lambda_handler(event, context):

  # Show the incoming event in the debug log
  print("Event received by Lambda function: " + json.dumps(event, indent=2))


  # Construct message to be sent
  message = 'Session Has Been Uploaded/Modified'
  print(message)

  # Send message to SNS
  sns.publish(TopicArn=snsTopicArn,
  Message=message,
  Subject='New Session Uploaded',
  MessageStructure='raw'
  )

  # Finished!
  return 'Successfully processed {} records.'.format(len(event['Records']))
