import json
import os
import boto3

s3 = boto3.client("s3")
bedrock = boto3.client("bedrock-runtime")

#BUCKET_NAME = os.environ["BUCKET_NAME"]
MODEL_ID = "amazon.nova-lite-v1:0"

SUMMARY_PROMPT_TEMPLATE = """
You are a careful technical summarizer.

You are given multiple partial summaries from a single conference presentation.
Your task is to produce a clear, coherent, end-to-end summary of the entire presentation.

Rules:
- Do NOT introduce new facts
- Do NOT hallucinate
- Preserve technical accuracy and terminology
- Prefer clarity over verbosity
- Output 6–10 bullet points maximum

Partial summaries:
{allChunksText}
"""

def lambda_handler(event, context):

    # 1. Find all matching chunk files
    prefix = event["partialFilename"]
    response = s3.list_objects_v2(
        Bucket = "reinvent-ml-pipeline-temp",
        Prefix = "_4_ summarised chunks/" + prefix
    )
    print(response)
    if "Contents" not in response:
        raise Exception(f"No chunk files found for prefix {prefix}")

    # 2. Read and concatenate chunk text
    chunkTexts = []
    for obj in sorted(response["Contents"], key=lambda x: x["Key"]):
        key = obj["Key"]
        if not key.endswith(".txt"):
            continue

        file_obj = s3.get_object(Bucket = "reinvent-ml-pipeline-temp", Key = key)
        text = file_obj["Body"].read().decode("utf-8").strip()
        chunkTexts.append(text)

    allChunksText = "\n\n".join(chunkTexts)

    # 3. Build prompt
    prompt = SUMMARY_PROMPT_TEMPLATE.format(
        allChunksText = allChunksText
    )
    print(prompt)

    # 4. Invoke Nova Light
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId = MODEL_ID,
        contentType = "application/json",
        accept = "application/json",
        body = json.dumps(body)
    )

    print(response)
    response_body = json.loads(response["body"].read())
    summary_text = response_body["output"]["message"]["content"][0]["text"]
    print(summary_text)

    # 5. Write final summary
    output_key = "_5_ summaries/" + event["partialFilename"] + "_summary.txt"
    s3.put_object(
        Bucket = "reinvent-ml-pipeline-temp",
        Key = output_key,
        Body = summary_text.encode("utf-8"),
        ContentType = "text/plain"
    )

    return {
        "status": "OK",
        "summaryKey": output_key
    }
