from random import randrange

import boto3
import json

def lambda_handler(event, context):
    sqs = boto3.client("sqs")
    dydb = boto3.resource("dynamodb")
    queue_url = 'https://sqs.ap-southeast-2.amazonaws.com/916589119438/MyQueue'
    
    response_sqs = sqs.receive_message(QueueUrl = queue_url, MaxNumberOfMessages = 1)
    operand_1 = int(response_sqs["Messages"][0]["Body"])
    operand_2 = randrange(100)

    table = dydb.Table("Sums")
    response_dydb = table.put_item(
        Item = {
            'DateTime': response_sqs["ResponseMetadata"]["HTTPHeaders"]["date"],
            'operand_1': operand_1,
            'operand_2': operand_2,
            'sum': (operand_1 + operand_2)
        }
    )

    response_sqs = sqs.delete_message(QueueUrl = queue_url, ReceiptHandle = response_sqs["Messages"][0]["ReceiptHandle"])

    return {
        'statusCode': 200,
    }