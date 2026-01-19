# Reinvent summariser
Talk URL-> yt_dlp running in ECS (subtitles -> chunks) -> summarised chunks -> summarised talk.

To install
* Build the docker image for ARM64, upload to ECR.
- I ended up doing this with CodeBuild, which took ~10 mins on the first run (hopefully it caches for next time). I want ARM64 for Graviton, and emulating that on my MacBook was not working.
- Note that the relative directories and resulting docker build command lines - I arrived at these by trial and error.
* Instantiate the Stack, give the ARN of the Containerized Image as a parameter.

TODO:
* Build out the codebuild project. That is - take the ECR repo as an arg to the stack, then define and build the codebuild project, then create a custom resource which upon creation: runs the build job, then make the Task definition or possibly the Task itself as DependsOn the container image.
* Also - make the stack define the ECR repo. Until then - parameterize its ARN as an input.
* Also - include a s3 bucket to serve as a cache.
* I had to build a sec grp with outbound 443, and a log group to match what was in the config.

* SPlit the buildspecs into two - so I don't need 10 mins every time i mess with my python code. I.e. a base image built infrequently, and then an interactive image built from the former.


sam build
sam deploy \
  --stack-name reinvent-pipeline \
  --s3-bucket reinvent-pipeline-pipelineoutputbucket-uw7w6y69rnw8 \
  --region ap-southeast-2 \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \



