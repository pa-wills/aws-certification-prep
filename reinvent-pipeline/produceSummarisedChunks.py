import os
import json
import time
import boto3

REGION = "ap-southeast-2"
MODEL_ID = "amazon.nova-micro-v1:0"

INPUT_ROOT =  "/Users/pwills/Desktop/reinvent 2025/_3_ Chunked, cleaned summaries/Technical Breakout Sessions/End-User Computing"
OUTPUT_ROOT = "/Users/pwills/Desktop/reinvent 2025/_4_ Summarised chunks/Technical Breakout Sessions/End-User Computing"

# Bedrock rate limiting (very important)
DELAY_SECONDS = 0.5  # adjust to avoid throttling

bedrock = boto3.client("bedrock-runtime", region_name=REGION)

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

# -----------------------------
# Functions
# -----------------------------
def summarise_text(chunk_text):
    prompt = SUMMARY_PROMPT_TEMPLATE.format(chunkText = chunk_text)

    body = {
        "messages": [
            {
            	"role": "user", 
            	"content": [{"text": prompt}]
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
#    print(result)
    return result["output"]["message"]["content"][0]["text"].strip()

def process_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        chunk_text = f.read()

    summary = summarise_text(chunk_text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

def recurse_and_summarise(input_root, output_root):
    for root, _, files in os.walk(input_root):
        for file in files:
            if file.endswith(".txt"):
                input_path = os.path.join(root, file)

                rel_path = os.path.relpath(input_path, input_root)
                output_path = os.path.join(output_root, rel_path)

                print(f"Processing: {rel_path}")
                process_file(input_path, output_path)

                time.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    recurse_and_summarise(INPUT_ROOT, OUTPUT_ROOT)
