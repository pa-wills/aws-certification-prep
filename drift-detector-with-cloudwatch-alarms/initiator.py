from random import randrange

import boto3
import json
import os


def lambda_handler(event, context):
    sqsClient = boto3.client("sqs")
    cfClient = boto3.client('cloudformation')
    list = cfClient.list_stacks(StackStatusFilter = ["CREATE_COMPLETE", "UPDATE_COMPLETE", "IMPORT_COMPLETE"])
    print("list: " + str(list["StackSummaries"]))
    for stack in list["StackSummaries"]:
        print("stack: " + str(stack))
        stackDriftDetectionId = cfClient.detect_stack_drift(StackName = str(stack["StackName"]))
        print(stackDriftDetectionId["StackDriftDetectionId"])
        sqsClient.send_message(QueueUrl = os.environ['queueRef'], DelaySeconds = 5, MessageBody = str(stackDriftDetectionId["StackDriftDetectionId"]))
    return {
        'statusCode': 200,
    }