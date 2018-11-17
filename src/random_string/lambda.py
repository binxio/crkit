import base64
import json
import logging
import string
import random
import boto3
from botocore.vendored import requests
import cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def random_string(size=6):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def lambda_handler(event, context):
    logger.info('got event {}'.format(event))
    responseData = {}

    if event['RequestType'] == 'Create':
        number = int(event['ResourceProperties'].get('Number', 6))
        rs = random_string(number)
        responseData['upper'] = rs.upper()
        responseData['lower'] = rs.lower()

    else: # delete / update
        rs = event['PhysicalResourceId'] 
        responseData['upper'] = rs.upper()
        responseData['lower'] = rs.lower()
                    
    logger.info('responseData {}'.format(responseData))
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, responseData['lower'])
