# ChronojumpDataProcessor Lambda function
#
# This function is triggered by an object being created in an Amazon S3 bucket.
# The file is downloaded and each line is inserted into DynamoDB tables.

from __future__ import print_function
from decimal import Decimal
import json, urllib, boto3, csv, uuid
from datetime import datetime

AWS_REGION = "eu-west-1"

sess = boto3.Session(region_name=AWS_REGION)

# Connect to S3 and DynamoDB
cfnclient = sess.client('cloudformation')
s3c = sess.client('s3')
s3 = sess.resource('s3')
dynamodb = sess.resource('dynamodb')

# Connect to the DynamoDB tables
athleteTable = dynamodb.Table('Athlete')
countermovementTable = dynamodb.Table('CMJ')
depthTable = dynamodb.Table('DepthJump')

now = datetime.now()
date = now.strftime("%Y-%m-%d %H:%M:%S")

response = cfnclient.describe_stack_resource(
    StackName='ChronojumpStack',
    LogicalResourceId='InputS3BucketForChronojumpDataFiles'
)

resource = response['StackResourceDetail']
bucket_name = resource['PhysicalResourceId']

get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
objs = s3c.list_objects_v2(Bucket=bucket_name)['Contents']
last_added = [obj for obj in sorted(objs, key=get_last_modified)]
name = last_added[-1]['Key']

localFilename = '/tmp/' + name

# This handler is executed every time the Lambda function is triggered
def lambda_handler(event, context):

    # Show the incoming event in the debug log
    #print("Event received by Lambda function: " + json.dumps(event, indent=2))

    # Get the bucket and object key from the Event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')


    # Download the file from S3 to the local filesystem
    try:
        s3.meta.client.download_file(bucket, key, localFilename)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    # Read the Session CSV file. Delimiter is the ',' character
    with open(localFilename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        # Read each row in the file
        rowCount = 0
        for row in reader:
            rowCount += 1

            # Show the row in the debug log
            print(row['athlete_id'], row['athlete_name'], row['date_time'],
            row['jump_type'], row['jump_tc'], row['jump_height'], row['jump_RSI'])
            print(rowCount)
            
            try:
                # Insert Athlete ID and Name into Athlete DynamoDB table
                athleteTable.put_item(
                    Item={
                        'AthleteID':       row['athlete_id'],
                        'AthleteName':     row['athlete_name']})

                # Insert CMJ details into Countermovement Jump DynamoDB table
                if ((row['jump_type'] == "CMJ") & (Decimal(str(row['jump_height'])) >= 30) & (Decimal(str(row['jump_height'])) < 80) 
                | (row['jump_type'] == "Free") & (Decimal(str(row['jump_height'])) >= 30) & (Decimal(str(row['jump_height'])) < 80)) :
                    countermovementTable.put_item(
                        Item={
                            'AthleteID':           row['athlete_id'],
                            'AthleteName':         row['athlete_name'],
                            'DateTime':            row['date_time'].replace(" ", "_"),
                            'JumpType':            row['jump_type'],
                            'JumpID':              (uuid.uuid1().int>>64),
                            'Height':              Decimal(str(row['jump_height']))})
                elif ((row['jump_type'] == "RJ(j)")
                & (Decimal(str(row['jump_height'])) >= 30) & (Decimal(str(row['jump_height'])) <= 80) 
                & (Decimal(str(row['jump_RSI'])) >= 1.2)) :
                 
                    # Insert Depth Jump details into Depth Jump DynamoDB table
                    depthTable.put_item(
                        Item={
                            'AthleteID':            row['athlete_id'],
                            'AthleteName':          row['athlete_name'],
                            'DateTime':             row['date_time'].replace(" ", "_"),
                            'JumpType':             row['jump_type'],
                            'JumpID':               (uuid.uuid1().int>>64),
                            'ContactTime':          Decimal(str(row['jump_tc'])),
                            'Height':               Decimal(str(row['jump_height'])),
                            'RSI':                  Decimal(str(row['jump_RSI']))})
                
                    
            except Exception as e:
                 print(e)
                 print("Unable to insert data into DynamoDB table".format(e))

    # Finished!
    return "%d data inserted" % rowCount
                
