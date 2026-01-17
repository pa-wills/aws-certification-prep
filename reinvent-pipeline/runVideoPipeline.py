# pipeline/runVideoPipeline.py
import argparse
import os
#import boto3
#from pipeline.ingest import download_captions
from pipeline.transcript import vtt_to_text
from pipeline.process import chunk_text

import sys
print("Python started", flush = True)
print(sys.argv, flush=True)

parser = argparse.ArgumentParser()
parser.add_argument("vttFile", help="VTT file to be processed into chunked")
# parser.add_argument("--no-llm", action="store_true", help="Skip LLM summarization")
args = parser.parse_args()

# I'm removing the download captions element, because really - I don't need it anymore.
# For Reinvent the manual mechanism is not a major pain. I _could_ use Transcribe, but that's probably OTT.

# Download captions
#vtt_file = download_captions(args.url)

s3  = boto3.client("s3")
try:
    exists = s3.head_object(Bucket = "reinvent-ml-pipeline-temp", Key = args.vttFile) # TODO: parameterize
    print("Exists: ", exists)
    response = s3.get_object(Bucket = "reinvent-ml-pipeline-temp", Key = args.vttFile) # TODO: parameterize
    body = response["Body"]
except ClientErro as e:
    raise

# Convert VTT → clean text
text = vtt_to_text(body)

# Chunk text
chunks = chunk_text(text, chunkSize = 500)

# Write chunks to S3
#output_dir = "/app/output"
folderPath = "_3_ chunks/"
for i, chunk in enumerate(chunks, 1):
    fileName = str(((args.vttFile)[:-4])) + "_Chunk_" + str(i).zfill(4) + ".txt"
    S3Key = f"{folderPath}{fileName}"
    s3.put_object(Bucket = "reinvent-ml-pipeline-temp", Key = s3Key, Body = str(chunk))
#    chunk_file = os.path.join(
#        output_dir, f"{os.path.splitext(os.path.basename(vtt_file))[0]}_chunk{idx}.txt"
#    )
#    with open(chunk_file, "w", encoding="utf-8") as f:
#        f.write(chunk)

print(f"Created {len(chunks)} chunks. Done.")
