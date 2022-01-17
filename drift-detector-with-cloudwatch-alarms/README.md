 # Simple SQS Producer Consumer
This is a project to (1) autmotate periodic Drift Detection for all running CF Stacks, and (2) alert me in CloudWatch when it comes back red. So. A project with some enduring utility, but also a valuable opportunity to explore an unfamiliar Product.

Configuration drift is bad bad bad bad bad. And AWS usefully provides some promitives to help with this. AWS CloudFormation Drift Detection being the one I am most familiar with. AWS Config looks like a full CMDB implementation (though not with full AWS product coverage).


## Design
1. Lambda function with following logic: 1. detect all Stacks, 2. run detect_stack_drift() on all, 3. push Message to a SQS Queue with the associated StackDriftDetectionIDs. Control invocation with a scheduled EventBridge Event (and parameterise invocation periodicty).
2. Another Lambda function to poll the Queue, check Drfit Detection status. If DETECTION_IN_PROGRESS then backoff. If DETECTION_FAILED then probably DLQ. If DETECTION_COMPLETE, then inspect status. If DRIFTED note that in a DyDB Table, else take no action. Oh yeah, and TTL the Items.
3. Tabulate the status of the stacks.
4. Perhaps use DyDB Streams or the third lambda function itself to publish that metric.
5. Cloudwatch alarm if that metric > 0.

## For another time
* Automated corrective action.
* Incorporate Config.
* Notification?
* The basic inconsistency that DETECTION_FAILED can occur as well as IN_SYNC, and what to do about this.
* Hmm, to the extent that each stack contains Lambdas - perhaps I should [sign that code](https://aws.amazon.com/blogs/aws/new-code-signing-a-trust-and-integrity-control-for-aws-lambda/), and get the checker to verf the same. 
* Hmm, can i deploy a signed hash of the most recent commit of the repo?
* The alarm itself. I've exhausted my powers of concentration (such that they are) for the moment.


## Running it

    sam build
    sam package --s3-bucket drift-detector-with-cloudwatch-alarms-store
    sam deploy --stack-name drift-detector-with-cloudwatch --s3-bucket drift-detector-with-cloudwatch-alarms-store --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM
