	import boto3
	import datetime
	import json
	import os

	from boto3.dynamodb.conditions import Key, Attr

	# TODO: A bunch of this (not all) should really invoke on a table change, otherwise just write the previous value.

	def lambda_handler(event, context):
		# TODO: attach to the DyDB table.
		# Determine list of stacks. (I guess get a list of distinct StackIDs)
		# Find the most recent entry for each stack.
		# Count the number of not IN_SYNCs from this list.
		# Publish that stat.

		dyDbClient = boto3.resource('dynamodb')
		table = dyDbClient.Table(str(os.environ['dyDbNAme']))
		cwClient = boto3.client('cloudwatch')

		# Determine distinct StackIDs (not going to win prizes for efficiency here).
		entireTable = table.scan(TableName = str(os.environ['dyDbNAme']))
		print("Entire table" + str(entireTable))
		distinctStackIds = []
		for item in entireTable['Items']:
			if (item['StackId']) not in distinctStackIds:
				distinctStackIds.append(item['StackId'])
		print ("Distinct Stack IDs: " + str(distinctStackIds))

		# Look for most recent record. Is it IN_SYNC? If not - increment counter.
		# The sort key ought to do the work for me here.
		errorCount = 0
		for StackId in distinctStackIds:
			# This use of a Key is brilliant, because from the documentation you'd be building a string, and it's not clear how to escape a ':'
			# which is not great given ARNs...... Such a mess.
			mostRecentStatus = table.query(KeyConditionExpression = Key('StackId').eq(StackId), Limit = 1, ScanIndexForward = False)['Items'][0]['StackDriftStatus']
			print(str(StackId) + ": " + str(mostRecentStatus))
			if (mostRecentStatus != "IN_SYNC"): 
				errorCount = errorCount + 1
		print(errorCount)

		# Publish the metric
		metricData = [{"MetricName": "NumOutOfSync", "Value": errorCount, }]
		cwClient.put_metric_data(Namespace = os.environ['nameSpaceForMetric'], MetricData = metricData)

		return {
			'statusCode': 200,
		}