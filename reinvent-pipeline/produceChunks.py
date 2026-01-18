# pipeline/runVideoPipeline.py
import argparse
import os
import boto3
import sys

from botocore.exceptions import ClientError


def lambda_handler(event, context):
	filename = event["filename"]
	print("Python started", flush = True)
	print(filename)

	s3  = boto3.client("s3")
	try:
		exists = s3.head_object(Bucket = "reinvent-ml-pipeline-temp", Key = ("_2_ transcriptions/" + str(filename))) # TODO: parameterize
		print("Exists: ", exists)
		response = s3.get_object(Bucket = "reinvent-ml-pipeline-temp", Key = ("_2_ transcriptions/" + str(filename))) # TODO: parameterize
		body = response["Body"]
	except ClientError as e:
		raise

	# Convert VTT → clean text
	text = vtt_to_text(body)

	# Chunk text
	chunks = chunk_text(text, chunkSize = 500)

	# Write chunks to S3
	#output_dir = "/app/output"
	folderPath = "_3_ chunks/"
	for i, chunk in enumerate(chunks, 1):
		fileName = str(((filename)[:-4])) + "_Chunk_" + str(i).zfill(4) + ".txt"
		S3Key = f"{folderPath}{fileName}"
		s3.put_object(Bucket = "reinvent-ml-pipeline-temp", Key = S3Key, Body = str(chunk))

	print(f"Created {len(chunks)} chunks. Done.")

def vtt_to_text(body):
	text_lines = []
	for line in body.iter_lines():
		line = line.decode("utf-8")
		if line.strip() == "" or "-->" in line or line.startswith("WEBVTT"):
			continue
		text_lines.append(line.strip())
	text = " ".join(text_lines)
	return text

def chunk_text(text, chunkSize = 500):
	words = text.split()
	chunks = []
	for i in range(0, len(words), chunkSize):
		chunks.append(" ".join(words[i : i + chunkSize]))
	return chunks


