from random import randrange

import boto3
import datetime
import json

def lambda_handler(event, context):
    dydb = boto3.resource("dynamodb")
    print("Event:" + str(event))
    
    for record in event['Records']:
        print("Record:" + str(record))
        operand_1 = int(record["body"])
        operand_2 = randrange(100)

        sentTimeStampEpoch = int(int(record["attributes"]["SentTimestamp"]) / 1000)
        sentTimeStampStr = datetime.datetime.fromtimestamp(sentTimeStampEpoch)  

        ttl = int(datetime.datetime.now().timestamp()) + (3600 * 2) # I.e. Now + 2 hours. Row count should be < 100.

        table = dydb.Table("Sums")
        response_dydb = table.put_item(
            Item = {
                'DateTime': str(sentTimeStampStr),
                'operand_1': operand_1,
                'operand_2': operand_2,
                'sum': (operand_1 + operand_2),
                'ttl': ttl
            }
        )

        # Apparently I don't need to explicitly delete the messages. 
        # Lambda does it for me. Assuming successful processing.

#        response_sqs = sqs.delete_message(QueueUrl = queue_url, ReceiptHandle = response_sqs["Messages"][0]["ReceiptHandle"])
        return {
            'statusCode': 200,
        }
