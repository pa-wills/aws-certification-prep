# Reinvent summariser
Talk URL-> yt_dlp -> cleaning and chunking -> summarised chunks -> summarised talk.

# Pulling the VTTs
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

When applied to say Re:Invent 2025 - this yields a coorpus of > 1,000 VTTs and > 400MBs of uncompressed text (which is enormous).


# The Stack
For the moment the cleaning, chunking, and model invocation are all done through a Lambdas. Deploy that using SAM, I.e.

``
sam build
sam deploy --stack-name reinvent-pipeline --s3-bucket reinvent-pipeline-pipelineoutputbucket-uw7w6y69rnw8 --region ap-southeast-2 --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
``


# TODO:
- Implement the State Machine properly.


