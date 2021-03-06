# 1. Prerequisites

* Chronojump-AWS from https://github.com/smithaaron2000/chronojump-aws
* AWS Account with AWS Configuration complete on your machine (https://aws.amazon.com/account/)
* Configure AWS-CLI (https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
* Python3 (https://docs.python-guide.org/starting/install3/linux/)
* Grafana Account (https://grafana.com)

Alternative (Not Required)
* Podman installed (https://podman.io/getting-started/installation)
* Docker installed (https://www.docker.com/?utm_source=google&utm_medium=cpc&utm_campaign=search_emea_brand&utm_term=install_docker_exact&gclid=Cj0KCQjw06OTBhC_ARIsAAU1yOWdmiqTw5krqphLiOGA39yJOBnzd8tcG_nbj0ejqVkvNBObr_qIPq8aAnp5EALw_wcB)

# 2. Installing

Clone the project using the command:

```
git clone https://github.com/smithaaron2000/chrono-serverlessarchitecture
```
Or if you have an SSH Key:
```
git clone git@github.com:smithaaron2000/chrono-serverlessarchitecture.git
```

Alternatively, you could pull the image from DockerHub using the command:

```
podman pull docker.io/smithaaron2000/chrono-serverless-architecture
```
Or

```
docker pull docker.io/smithaaron2000/chrono-serverless-architecture
```

# 3. Creating an Amazon Athena Datasource

When asked to choose a datasource, select DynamoDB, and then select "Next".

![image](https://user-images.githubusercontent.com/43610720/164291749-55bc828e-9412-47e5-aa02-8ec2cc3c7a12.png)

Set the name of the data source to "Chronojump".

Under Connection Details, select "Create Lambda Function".

![image](https://user-images.githubusercontent.com/43610720/164292055-1a544266-07b9-4f90-96cd-e35c723ac446.png)

Create an S3 bucket to act as a spill bucket for the function to spill data, and enter the name of the bucket in the SpillBucket input.

![image](https://user-images.githubusercontent.com/43610720/164292248-3f6db40c-0121-4a21-a5aa-ca4d914e3be8.png)

On the Review and Create page, select "Create Data Source".

# 4. Creating the Serverless Architecture

The Architecture is created by running the following command:
```
python3 fullscript.py
```

Alternatively, if you pulled the image from DockerHub, run:
```
podman run -v ~/.aws:/root/.aws docker.io/smithaaron2000/chrono-serverless-architecture
```
Or
```
docker run -v ~/.aws:/root/.aws docker.io/smithaaron2000/chrono-serverless-architecture
```
Ensure that you have a config file in your ~/.aws/ folder, with your AWS region, your Access Key ID and your Secret Access Key in the config file.

This will create the following resources in AWS:
* S3 Bucket
* Lambda Function for processing CSVs uploaded to S3
* 3 DynamoDB Tables (Athlete, Countermovement Jump, Depth Jump)
* SNS Topic
* Lambda Function which is triggered by the DynamoDB tables being uploaded, which notifies the SNS Topic.
* Amazon Athena Workgroup (to allow Grafana to query DynamoDB tables).

# 5. Connecting Grafana Cloud to Amazon Athena
Navigate to the Grafana Plugins and install the plugin for Athena to your project.
https://grafana.com/grafana/plugins/grafana-athena-datasource/?tab=installation
Install the plugin onto Grafana Cloud.

On the Grafana dashboard on the left sidebar, hover over Configuration and select Data Sources.

![Screenshot from 2022-04-20 21-30-11](https://user-images.githubusercontent.com/43610720/164308455-c1accb43-4370-4dbe-9352-a94341463a3a.png)

On the Data Source page, select "Add data source".
Next, configure the data source.
![image](https://user-images.githubusercontent.com/43610720/164309387-f24169ef-3060-46e8-a227-fa5c92b4c848.png)

## Connection Details
* Select Access and Secret Key as the Authentication Provider.
* Input your Access Key ID and Secret Access Key.
* Select your AWS Region.

## Athena Details
* For data source, select Chronojump.
* For database, select default.
* For workgroup, select athenav2 (this was created for you in the serverless architecture).

Select "Save and Test". If the configuration is set up correctly, you wull see the following output:

![image](https://user-images.githubusercontent.com/43610720/164310614-813ed8c9-a82f-41ef-be3f-1ff4a1552cf2.png)

# 6. Creating the Dashboard
* On the left sidebar, hover over the + sign and select "Import".
* Upload the chronojump-grafana.json file. 
* NOTE: replace any instance of $INSERT_NAME_HERE with the name of an athlete in your database (For Individual Progression Charts).

If configuration is successful, the dashboard will be available, looking like this:

![image](https://user-images.githubusercontent.com/43610720/164314848-06a07708-9e25-4a62-ac74-ab27f5983cf7.png)

# 7 . Uploading to the Serverless Architecture

* In your Desktop, create a folder called "ChronojumpCSVs". This is the folder where the CSV files are uploaded from.
* In Chronojump after completing and saving a session, navigate to the settings button.

![image](https://user-images.githubusercontent.com/43610720/165109017-33604cce-9692-4186-8022-32e19dd68a69.png)

* Click on "More", and choose "Export to CSV".

![image](https://user-images.githubusercontent.com/43610720/165109120-41edeb53-705c-4eca-a4c8-15d9208262e0.png)

* Select the "Chronojump CSVs" folder, and press export.




