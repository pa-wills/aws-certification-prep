# Simple Glue application
S3 bucket (which auto-downloads the Iris dataset) -> Glue Crawler -> Glue ETL -> Searchable Parquet.

To make it work: 1. Run the Glue Crawler and verify the outputted columns match those in the input dataset, 2. Run the GLue ETL Job and verify that the outputted data in S3 is in Parquet format (use Athena).

To delete: remove all the files from the S3 bucket then delete the Stack.
