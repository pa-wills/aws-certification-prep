import boto3
import datetime
import json
import os

def lambda_handler(event, context):
    cfClient = boto3.client('cloudformation')
    dyDbClient = boto3.resource('dynamodb')
    table = dyDbClient.Table(str(os.environ['dyDbNAme']))

    # This loop should be superfluous. I set the batch size to 1.
    for record in event['Records']:
        stackDriftDetectionId = record["body"]

        # Is it complete?
        status = cfClient.describe_stack_drift_detection_status(StackDriftDetectionId = stackDriftDetectionId)
        print(status)
        detectionStatus = str(status["DetectionStatus"])
        assert ((detectionStatus in ['DETECTION_IN_PROGRESS','DETECTION_FAILED', 'DETECTION_COMPLETE']) == True), "Invalid Detection Status"
        if (detectionStatus == 'DETECTION_IN_PROGRESS'):
            raise Exception('Detection is incomplete (returning message to queue).')

        # NOTE: I am noticising that DDs can come back "DETECTION_FAILED" and yet "IN_SYNC". It means that one or more 
        # of the resources have failed to evaluate Drift. But - because a DD has previously been ok - the Stack and Resource
        # still yield IN_SYNC. So. I am going to re-write the code to allow for this.
        # TODO: Secondary scan for DDs that come back DETECTION_FAILED - should kick off a resource-level check, and perhaps
        # we alarm in situations where the last IN_SYNC was / is > 2 days earlier, or similar.

        # OK, so it's no longer DETECTION_IN_PROGRESS. What's the result?
        driftStatus = status["StackDriftStatus"]
        assert (driftStatus in ['DRIFTED','IN_SYNC','UNKNOWN', 'NOT_CHECKED']), "Invalid Drift Status"
        if (driftStatus == 'IN_SYNC'):
            print("In Sync! " + str(status))
        elif (driftStatus in ['UNKNOWN', 'NOT_CHECKED']):
            print("Unexpected status! " + str(status))
#            raise Exception('Drift status inconsistent with Detection status (returning mesage to queue).')
        elif (driftStatus == 'DRIFTED'):
            # TODO: If "DRIFTED", then we're pushing that state to a DyDB table. Use TTL so old checks auto-expire.
            print("Drift detected! " + str(status))

        # TODO: Regardless - compute the total number of confirmed drifted stacks, and publish the metric.
        # INVARIANT: if that metric computes to > 0, an alarm should raise.
        ttl = int(datetime.datetime.now().timestamp()) + (3600 * 24 * 7) # I.e. Now + 7 days. 
        response_dydb = table.put_item(
            Item = {
                'StackId': str(status['StackId']),
                'StackDriftStatus': str(status['StackDriftStatus']),
                'DetectionStatus': str(status['DetectionStatus']),
                'Timestamp': str(status['Timestamp']),
                'ttl': ttl
            }
        )

    return {
        'statusCode': 200,
    }