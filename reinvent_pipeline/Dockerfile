# Start from a Python image
FROM public.ecr.aws/docker/library/python:3.11-slim

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg curl && rm -rf /var/lib/apt/lists/*

# Install yt-dlp
RUN pip install --upgrade yt-dlp openai tiktoken python-dotenv rich pydantic

# Copy your pipeline code
WORKDIR /app
COPY pipeline /app/pipeline
COPY runVideoPipeline.py /app/runVideoPipeline.py

ENV PYTHONPATH=/app

ENTRYPOINT ["python", "runVideoPipeline.py https://www.youtube.com/watch?v=Ny4rrINHPe0"]
