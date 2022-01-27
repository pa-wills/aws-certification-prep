from random import randrange

import aws_xray_sdk
import boto3
import datetime
import json
import os

from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

def lambda_handler(event, context):
    dydb = boto3.resource("dynamodb")
    print("Event:" + str(event))
    
    for record in event['Records']:
        print("Record:" + str(record))
        operand_1 = int(record["body"])
        operand_2 = randrange(100)

        sentTimeStampEpoch = int(int(record["attributes"]["SentTimestamp"]) / 1000)
        sentTimeStampStr = datetime.datetime.fromtimestamp(sentTimeStampEpoch)  

        ttl = int(datetime.datetime.now().timestamp()) + (3600 * 2) # I.e. Now + 2 hours. 
        # INVARIANT: Row count should be ~<= 60 due to TTL.

        table = dydb.Table(os.environ['tableRef'])
        Item = {
            'DateTime': str(sentTimeStampStr),
            'operand_1': operand_1,
            'operand_2': operand_2,
            'sum': (operand_1 + operand_2),
            'ttl': ttl
        }
        print(Item)
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
        return {
            'statusCode': 200,
            'response_dydb': json.dumps(str(response_dydb))
        }
