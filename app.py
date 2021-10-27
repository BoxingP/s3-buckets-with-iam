#!/usr/bin/env python3
import os
import yaml

from aws_cdk import core as cdk
from s3_buckets_with_iam.iam_stack import IAMStack
from s3_buckets_with_iam.s3_bucket_stack import S3BucketStack

with open('aws_tags.yaml', 'r', encoding='UTF-8') as file:
    aws_tags = yaml.load(file, Loader=yaml.SafeLoader)
project = aws_tags['project'].lower().replace(' ', '-')
environment = aws_tags['environment']

app = cdk.App()
s3_bucket_stack = S3BucketStack(app, '-'.join([project, environment, 's3']),
                                env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                                    region=os.getenv("CDK_DEFAULT_REGION")))
iam_stack = IAMStack(app, '-'.join([project, environment, 'iam']),
                     s3_bucket_stack.to_casmart_bucket, s3_bucket_stack.to_thermofisher_bucket,
                     s3_bucket_stack.config_db_bucket, s3_bucket_stack.logs_bucket,
                     env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
                                         region=os.getenv("CDK_DEFAULT_REGION")))

for key, value in aws_tags.items():
    cdk.Tags.of(app).add(key, value or " ")
cdk.Tags.of(s3_bucket_stack).add("application", "S3 Bucket")
cdk.Tags.of(iam_stack).add("application", "IAM")
app.synth()
