import logging
import boto3
import cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    try:
        bucket = event['ResourceProperties']['BucketName']
        if event['RequestType'] == 'Delete':
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(bucket)
            for obj in bucket.objects.filter():
                s3.Object(bucket.name, obj.key).delete()
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})

    except Exception as e:
        print(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})
