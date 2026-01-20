import json
import os
import boto3
from collections import defaultdict

# ---------- Config ----------
INPUT_ROOT =  "/Users/pwills/Desktop/reinvent 2025/_4_ Summarised chunks/"
OUTPUT_ROOT = "/Users/pwills/Desktop/reinvent 2025/_5_ Summaries/"
MODEL_ID = "amazon.nova-lite-v1:0"

bedrock = boto3.client("bedrock-runtime")

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
# ----------------------------

def summary_exists(input_root, output_root, group_root, prefix):
    relative_path = os.path.relpath(group_root, input_root)
    output_dir = os.path.join(output_root, relative_path)
    output_file = os.path.join(output_dir, f"{prefix}_summary.txt")
    return os.path.exists(output_file)

def find_chunk_groups(root_dir):
    """
    Walks the directory tree and groups chunk files by prefix.
    Returns:
      { prefix: [full_path1, full_path2, ...] }
    """
    groups = defaultdict(list)

    for root, _, files in os.walk(root_dir):
        for filename in files:
            if not filename.endswith(".txt"):
                continue
            if "_chunk_" not in filename:
                continue

            prefix = filename.split("_chunk_")[0]
            full_path = os.path.join(root, filename)
            groups[(root, prefix)].append(full_path)

    # Sort each group's file list so chunks are in correct order
    for key in groups:
        groups[key].sort()

    return groups


def load_chunks(chunk_files):
    texts = []
    for path in sorted(chunk_files):
        with open(path, "r", encoding="utf-8") as f:
            texts.append(f.read().strip())
    return "\n\n".join(texts)


def invoke_bedrock(prompt):
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
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    response_body = json.loads(response["body"].read())
    return response_body["output"]["message"]["content"][0]["text"].strip()


def write_summary(input_root, output_root, group_root, prefix, summary_text):
    relative_path = os.path.relpath(group_root, input_root)
    output_dir = os.path.join(output_root, relative_path)
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{prefix}_summary.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"\033[32m✔ Wrote summary: {output_file}\033[0m")


def main():
    groups = find_chunk_groups(INPUT_ROOT)
    if not groups:
        raise RuntimeError("No chunk groups found.")

    for (group_root, prefix), chunk_files in groups.items():
        print(f"\nProcessing: {prefix}")
        if summary_exists(INPUT_ROOT, OUTPUT_ROOT, group_root, prefix):
            print(f"\033[33m⏭️ Summary already exists for {prefix}, skipping.\033[0m")
            continue

        all_chunks_text = load_chunks(chunk_files)

        prompt = SUMMARY_PROMPT_TEMPLATE.format(
            allChunksText=all_chunks_text
        )

#        print(prompt)

        summary = invoke_bedrock(prompt)
#        summary = "some bullshit"

        write_summary(
            INPUT_ROOT,
            OUTPUT_ROOT,
            group_root,
            prefix,
            summary
        )


if __name__ == "__main__":
    main()
