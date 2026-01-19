import json
import boto3
import os

#from botocore.exceptions import ClientError


s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime", region_name="ap-southeast-2")

MODEL_ID = "amazon.nova-micro-v1:0"

SUMMARY_PROMPT_TEMPLATE = """
You are a careful, technical summarizer.

Task:
- Summarize the text below into exactly 5 bullet points.
- Do NOT add any new information or guess anything not present.
- Preserve technical terms and key facts.
- Keep each bullet short (1–2 sentences max).
- If the text contains no useful content, return "NO_CONTENT".

Text:
{chunkText}
"""


def lambda_handler(event, context):
	filename = event["filename"]
	obj = s3.get_object(Bucket = "reinvent-ml-pipeline-temp", Key = ("_3_ chunks/" + str(filename)))
	chunkText = obj["Body"].read().decode("utf-8")

	prompt = SUMMARY_PROMPT_TEMPLATE.format(chunkText = chunkText)
	print(prompt)
	body = {
		"messages": [
			{
				"role": "user", 
				"content":  prompt
			}
		]
	}

	response = bedrock.invoke_model(
		modelId = MODEL_ID,
		contentType = "application/json",
		accept = "application/json",
		body = json.dumps(body)
	)

	result = json.loads(response["body"].read())
	summary_text = result["results"][0]["outputText"].strip()
	print(summary_text)

	# 4. Write summary back to S3
	summary_key = key.replace("_3_ transcriptions/", "_4_ summarised chunks/")

	s3.put_object(
		Bucket = "reinvent-ml-pipeline-temp",
		Key = summary_key,
		Body = summary_text.encode("utf-8"),
		ContentType = "text/plain"
	)

	return {
		"status": "ok",
		"input": key,
		"output": summary_key
	}
