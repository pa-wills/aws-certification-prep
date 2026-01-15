# pipeline/runVideoPipeline.py
import argparse
import os
from pipeline.ingest import download_captions
from pipeline.transcript import vtt_to_text
from pipeline.process import chunk_text

import sys
print("Python started", flush = True)
print(sys.argv, flush=True)

parser = argparse.ArgumentParser()
parser.add_argument("url", help="YouTube video URL")
parser.add_argument("--no-llm", action="store_true", help="Skip LLM summarization")
args = parser.parse_args()

# Download captions
vtt_file = download_captions(args.url)

# Convert VTT → clean text
text_file = vtt_to_text(vtt_file)

# Chunk text
chunks = chunk_text(text_file)

# Write chunks to disk
output_dir = "/app/output"
os.makedirs(output_dir, exist_ok=True)
for idx, chunk in enumerate(chunks, 1):
    chunk_file = os.path.join(
        output_dir, f"{os.path.splitext(os.path.basename(vtt_file))[0]}_chunk{idx}.txt"
    )
    with open(chunk_file, "w", encoding="utf-8") as f:
        f.write(chunk)


print(f"Created {len(chunks)} chunks. Done.")

# Only invoke LLM if not skipping
if not args.no_llm:
    from pipeline.llm import summarize_chunks
    summarize_chunks(chunks)
