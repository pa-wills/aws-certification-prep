# Simple SQS Producer Consumer
This is a project to demonstrate (I hope) that I know how to use SQS. It's a really simple use case.

* Producer fires every x seconds, generates number between 1..100, pushes message with said number to queue.
* Consumer polls said queue, retreieves message, gets number, adds another number between 1..100 to it, writes output to a DyDB table, deletes message from said queue.
* And I may mess with this a little to experiment with the edge cases.
* I'll define it into a Stack that I can deploy with the sam command line tools. Defining a CI/CD pipeline feels like overkill.


## Making it work
Use the usual [sam](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html) commands, and ensure of course that you have an appropriately privileged User configured for these actions.

	sam build
	sam package --s3-bucket simple-sqs-producer-consumer-store 
	sam deploy --stack-name simple-sqs-producer-consumer --s3-bucket simple-sqs-producer-consumer-store --capabilities CAPABILITY_NAMED_IAM CAPABILITY_IAM

(obviously use your own params for your S3 bucket and your stack's name)


