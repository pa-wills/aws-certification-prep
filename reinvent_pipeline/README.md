# Reinvent summariser
Talk URL-> yt_dlp running in ECS (subtitles -> chunks) -> summarised chunks -> summarised talk.

To install
* Build the docker image for ARM64, upload to ECR.
- I ended up doing this with CodeBuild, which took ~10 mins on the first run (hopefully it caches for next time). I want ARM64 for Graviton, and emulating that on my MacBook was not working.
- Note that the relative directories and resulting docker build command lines - I arrived at these by trial and error.
* Instantiate the Stack, give the ARN of the Containerized Image as a parameter.

TODO:
* Build out the 
* I had to build a sec grp with outbound 443, and a log group to match what was in the config.
