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

## Layering for X-Ray
I've decided to use this application as a test-bed for X-Ray. In doing so - I'm binding the project to a certain version of the X-Ray SDK, with the usual bloating that brings (my kB scale code zip is now > 10 MB). In order to make that more mamageable - I am experimenting with [this approach](https://github.com/matwerber1/python-aws-lambda-layer-aws-xray-sdk) and externalising the dep into a Layer.

[Here](https://aws.plainenglish.io/creating-aws-lambda-layer-for-python-runtime-1d1bc6c5148d) is the article that finally explained to me how to package and deploy layers. Starting from the directory with the lambda source code:

	mkdir python
	cd python
	pip3 install -t . aws_xray_sdk
	rm -r *dist-info __pycache__
	cd ..
	zip -r layer.zip python

(then upload to S3)

	rm layer.zip
	rm -rf python