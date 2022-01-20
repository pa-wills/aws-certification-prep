import boto3
import json
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

lambdaClient = boto3.client('lambda')
lambdaClient.get_account_settings()

def lambda_handler(event, context):
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    sqsClient = boto3.client("sqs")
    queue_url = 'https://sqs.ap-southeast-2.amazonaws.com/916589119438/MyQueue'
    number = randrange(100)
    sqsClient.send_message(QueueUrl = queue_url, DelaySeconds = 5, MessageBody = str(number))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }