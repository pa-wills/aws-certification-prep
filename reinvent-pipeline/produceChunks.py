# pipeline/runVideoPipeline.py
import argparse
import os
#import boto3
import sys
import re

#from botocore.exceptions import ClientError

import os
import re

def chunk_text(text, chunk_size=500):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])


def recurse_and_chunk(base_input_dir, base_output_dir, chunk_size=500):
    for root, _, files in os.walk(base_input_dir):
        for file in files:
            if file.endswith(".txt"):   # change to .vtt if needed
                input_path = os.path.join(root, file)

                # Preserve directory structure
                rel_path = os.path.relpath(input_path, base_input_dir)
                base_output_path = os.path.join(base_output_dir, rel_path).replace(".txt", "")

                # Read file
                with open(input_path, "r", encoding="utf-8") as f:
                    text = f.read()

                # Create output directory
                output_dir = os.path.dirname(base_output_path)
                os.makedirs(output_dir, exist_ok=True)

                # Chunk and write
                for idx, chunk in enumerate(chunk_text(text, chunk_size), start=1):
                    chunk_filename = f"{os.path.basename(base_output_path)}_chunk_{idx:04d}.txt"
                    chunk_path = os.path.join(output_dir, chunk_filename)

                    with open(chunk_path, "w", encoding="utf-8") as cf:
                        cf.write(chunk)


if __name__ == "__main__":
    base_input_dir =  "/Users/pwills/Desktop/reinvent 2025/_2_ Cleaned summaries/"
    base_output_dir = "/Users/pwills/Desktop/reinvent 2025/_3_ Chunked, cleaned summaries/"

    recurse_and_chunk(base_input_dir, base_output_dir, chunk_size=500)

