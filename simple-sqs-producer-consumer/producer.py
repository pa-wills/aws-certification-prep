from random import randrange

import boto3
import json
import os

def lambda_handler(event, context):
    sqsClient = boto3.client("sqs")
    number = randrange(100)
    sqsClient.send_message(QueueUrl = os.environ['queueRef'], DelaySeconds = 5, MessageBody = str(number))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }