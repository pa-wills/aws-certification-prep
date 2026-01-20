# Reinvent summariser
Talk URL-> yt_dlp -> cleaning -> chunking -> summarised chunks (w/ Bedrock) -> summarised talks (w/ Bedrock).

I had initially conceived this as a full AWS e2e stack, replete with Step functions, subordinate lamdas, etc. But - it turns out that that's overkill. Instead I do all of the processing localling, and my only AWS touches are the inferences performed by Bedrock.

The pipeline is:

1. Pull the VTTs for the individual talks.
2. Clean the VTTs into continuous text, suitable for summarisation.
3. Chunk the text.
4. Invoke Bedrock to produce summaries of the chunks.
5. Invoke Bedrock to produce summaries of the talks from those summarised chunks.


# 1. Pulling the VTTs
I had tried to AWS'ify the download of the VTTs into a dockerized micro-service, but it was over-kill (it's in the early commits FWIW). Far easier is to just stand-up a python virtual environment (in my case on my mac), configure yt_dlp, and then download the playlists one at a time. I.e.

``
python3 -m venv venv
source venv/bin/activate
pip install yt-dlp
yt-dlp --version
``

and then, for each playlist:

``
python3 -m yt_dlp \
  --no-check-certificate \
  --skip-download \
  --write-auto-sub \
  --sub-format vtt \
  --sleep-interval 10 \
  -o "/Users/pwills/Desktop/reinvent vtts/Global Sessions/%(playlist_index)s - %(title)s [%(id)s].%(ext)s" \
  "https://www.youtube.com/watch?v=CL3Sw4CTpEM&list=PL2yQDdvlhXf_a2j2zDfBKUciw_kQrPW4D"
``

When applied to say Re:Invent 2025 - this yields a corpus of > 1,000 VTTs and > 400MBs of uncompressed text (which is enormous).


# 2. Cleaning the VTTs (I.e. produceCleanTranscripts.py)
The VTTs need to be cleansed of VTT artifacts that would otherwise interfere with inference. For example: timestamp information, various tags, repeated sentences.

Executing this step produces the same number of files as the prior stage. But - the total size of the uncompressed text summaries was ~1 tenth that of the previous stage (for Re:Invent 2025).


# 3. Chunking the Cleaned Transcripts (I.e. produceChunks.py)
We then need to chunk that data. That is - split the outputs from the former stage into smaller files, each comprising a maximum number of words (I use 500 as a default). 


# 4. Summarising the cleaned chunks (I.e. produceSummarisedChunks.py)
Now we're going to use the cheapest of cheap Nova models to summarise those individual chunks. 

Two notes on this stage. Firstly we're going to use AWS services through boto3. I like to ensure this is going to work by using a venv. So, similar to before:

``
python3 -m venv ~/venvs/reinvent
source ~/venvs/reinvent/bin/activate
pip install boto3
python3 produceSummarisedChunks.py
``

Secondly, you'll need to configure the AWS CLI in order for any of this to work, and whatever Identity you're using will need to be allowed to invoke bedrock:InvokeModel on resource resource: arn:aws:bedrock:ap-southeast-2::foundation-model/amazon.nova-micro-v1:0


# 5. Reducing the summarised chunks to an overall summary for each talk (I.e. produceSummaries.py)






# TODO:
- Implement the State Machine properly.


