# Simple KDS application
Lambda producer (scheduled) -> KDS -> Lambda consumer (with event-source mapping).

Expected result: ordering preserved within the Shard (of which there is only one anyway) and its Partition. Verify by checking the time-stamp for same partition-key in the Consumer's Cloudwatch Logs.