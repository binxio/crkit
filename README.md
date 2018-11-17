# AWS CloudFormation Custom Resources Kit (crkit)

List of function available in this package

* RandomString
* EmptyS3Bucket

## Functions

### Random String

Some services in AWS cannot create a random name. Use this service to generate a random string to give the resource a random name. 

Properties:

* `Number` (not required): Length of the string to return

Return Values:

* `!Ref RandomStringLogicID`: Returns the random string in uppercase
* `!GetAtt RandomStringLogicID.lower`: Returns the random string in lowercase
* `!GetAtt RandomStringLogicID.upper`: Returns the rarndom string in uppercase

```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "mybucket-${RandomString.lower}"
  RandomString:
    Type: Custom::RandomString
    Properties:
      ServiceToken:
        !Sub "arn:aws:lambda:${AWS::Region}:${AWS::AccountId}:function:crkit-random-string"
      Number: 8
```

### Empty S3 Bucket

Deletes all files in an S3 Bucket before deleting. This is mainly useful when a bucket is created in a test environment and you would like to delete the bucket and it contents.

Properties:

* `BucketName` (required): Name of the bucket to empty

Return Values:

N/A

```yaml
Resources:
  S3Bucket:
    Type: AWS::S3::Bucket
  EmptyS3BucketOnDeletion:
    Type: Custom::EmptyS3Bucket
    Properties:
      ServiceToken:
        !Sub "arn:aws:lambda:${AWS::Region}:${AWS::AccountId}:function:crkit-empty-s3-bucket"
      BucketName: !Ref S3Bucket
```

## Deploy

Updating existing functions does not work currently. Delete the stack and create a new one is the easiest way. 

[![](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home?region=eu-west-1#/stacks/new?stackName=crkit&templateURL=https://s3-eu-west-1.amazonaws.com/binxio-public-eu-west-1/crkit/template.yml)

Or use the AWS CLI (to update, replace `create-stack` by `update-stack`)

```
VERSION=`cat version.txt`
REGION=eu-west-1
S3_BUCKET=binxio-public-$REGION
aws cloudformation create-stack \
  --stack-name crkit \
  --template-url https://s3-$REGION.amazonaws.com/$S3_BUCKET/crkit/template.yml \
  --capabilities CAPABILITY_IAM \
  --region eu-west-1 \
  --parameters ParameterKey=Version,ParameterValue=$VERSION \
               ParameterKey=S3Bucket,ParameterValue=$S3_BUCKET
```

## Pull Requests

Do you want your Custom Resource to be part of the crkit? Please make a pull request.

1. Clone this repo
2. Add your Lambda function to src/your_lambda_name/
3. Add your Lambda function and Role (if needed) to: template.yml
4. Add the documentation to README.md
5. Test the deployment by updating your own crkit and use the Lambda function
6. Send a Pull Request to review your function

## Tips for building Custom Resources

These packages are available in Lambda by default, so you won't have to add them to the requirements.txt and package them.

Except maybe for newer versions! Boto3 in Lambda is most of the time a few weeks or months old. So if you want to create a custom resource to start expirimenting with a brand new service or feature, you want the latest boto3 with your package.

```python
import base64
import json
import logging
import string
import random
import boto3
from botocore.vendored import requests
```
