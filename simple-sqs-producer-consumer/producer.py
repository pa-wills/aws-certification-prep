from random import randrange

import boto3
import json

def lambda_handler(event, context):
    client = boto3.client("sqs")
    queue_url = 'https://sqs.ap-southeast-2.amazonaws.com/916589119438/MyQueue'
    number = randrange(100)
    client.send_message(QueueUrl = queue_url, DelaySeconds = 5, MessageBody = str(number))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }