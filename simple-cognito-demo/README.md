# Simple Cognito application
S3 bucket website -> CFront (for HTTPS) -> Cognito for auth.

To make it work: 1. Instantiate the Stack and then create a OAC for the CFront Distribution then apply the generated Policy to the S3 bucket (TODO: I need to define the OAC and Bucket Policy statically in the template file).

