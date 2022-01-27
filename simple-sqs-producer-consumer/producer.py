from random import randrange

import aws_xray_sdk
import boto3
import json
import os

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    sqsClient = boto3.client("sqs")
    number = randrange(100)
    sqsClient.send_message(QueueUrl = os.environ['queueRef'], DelaySeconds = 5, MessageBody = str(number))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
