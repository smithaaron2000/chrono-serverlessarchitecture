1. Prerequisites

* Chronojump-AWS from https://github.com/smithaaron2000/chronojump-aws
* AWS Account with AWS Configuration complete on your machine (https://aws.amazon.com/account/)
* Python3 (https://docs.python-guide.org/starting/install3/linux/)
* Grafana Account (https://grafana.com)

2. Installing

Clone the project using the command:

```
git clone https://github.com/smithaaron2000/chrono-serverlessarchitecture
```
Or if you have an SSH Key:
```
git clone git@github.com:smithaaron2000/chrono-serverlessarchitecture.git
```

3. Creating an Amazon Athena Datasource

When asked to choose a datasource, select DynamoDB, and then select "Next".

![image](https://user-images.githubusercontent.com/43610720/164291749-55bc828e-9412-47e5-aa02-8ec2cc3c7a12.png)

Create a name for the datasource.

Under Connection Details, select "Create Lambda Function".

![image](https://user-images.githubusercontent.com/43610720/164292055-1a544266-07b9-4f90-96cd-e35c723ac446.png)

Create an S3 bucket to act as a spill bucket for the function to spill data, and enter the name of the bucket in the SpillBucket input.

![image](https://user-images.githubusercontent.com/43610720/164292248-3f6db40c-0121-4a21-a5aa-ca4d914e3be8.png)

On the Review and Create page, select "Create Data Source".

4. Creating the Serverless Architecture

The Architecture is created by running the following command:
```
python3 fullscript.py
```

This will create the following resources in AWS:
* S3 Bucket
* Lambda Function for processing CSVs uploaded to S3
* 3 DynamoDB Tables (Athlete, Countermovement Jump, Depth Jump)
* SNS Topic
* Lambda Function which is triggered by the DynamoDB tables being uploaded, which notifies the SNS Topic.
* Amazon Athena Workgroup (to allow Grafana to query DynamoDB tables).

5. Connecting Grafana to Amazon Athena


