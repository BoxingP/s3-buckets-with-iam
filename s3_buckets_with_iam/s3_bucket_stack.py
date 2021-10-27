from aws_cdk import (
    aws_s3 as s3,
    core as cdk
)


class S3BucketStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        access_logs_bucket = s3.Bucket(self, construct_id + "access",
                                       bucket_name=construct_id + "-bucket-access-logs", versioned=True,
                                       removal_policy=cdk.RemovalPolicy.DESTROY, auto_delete_objects=False,
                                       block_public_access=s3.BlockPublicAccess.BLOCK_ALL)

        to_casmart_bucket = s3.Bucket(self, construct_id + "casmart",
                                      bucket_name=construct_id + "-data-to-casmart", versioned=True,
                                      removal_policy=cdk.RemovalPolicy.DESTROY, auto_delete_objects=False,
                                      server_access_logs_bucket=access_logs_bucket, server_access_logs_prefix="casmart")

        to_thermofisher_bucket = s3.Bucket(self, construct_id + "thermofisher",
                                           bucket_name=construct_id + "-data-to-thermofisher", versioned=True,
                                           removal_policy=cdk.RemovalPolicy.DESTROY, auto_delete_objects=False,
                                           server_access_logs_bucket=access_logs_bucket,
                                           server_access_logs_prefix="thermofisher")

        config_db_bucket = s3.Bucket(self, construct_id + "config",
                                     bucket_name=construct_id + "-config-db-backup", versioned=True,
                                     removal_policy=cdk.RemovalPolicy.DESTROY, auto_delete_objects=False,
                                     server_access_logs_bucket=access_logs_bucket, server_access_logs_prefix="config")

        logs_bucket = s3.Bucket(self, construct_id + "logs",
                                bucket_name=construct_id + "-log", versioned=True,
                                removal_policy=cdk.RemovalPolicy.DESTROY, auto_delete_objects=False,
                                server_access_logs_bucket=access_logs_bucket, server_access_logs_prefix="log")

        self.lifecycle_rules(access_logs_bucket, expiration=365, noncurrent_expiration=14)
        self.lifecycle_rules(to_casmart_bucket, is_transition=False, expiration=7, noncurrent_expiration=7)
        self.lifecycle_rules(to_thermofisher_bucket, is_transition=False, expiration=30, noncurrent_expiration=30)
        self.lifecycle_rules(config_db_bucket, is_transition=False, expiration=30, noncurrent_expiration=30)
        self.lifecycle_rules(logs_bucket, expiration=180, noncurrent_expiration=14)
        self.to_casmart_bucket = to_casmart_bucket
        self.to_thermofisher_bucket = to_thermofisher_bucket
        self.config_db_bucket = config_db_bucket
        self.logs_bucket = logs_bucket

    @staticmethod
    def lifecycle_rules(bucket, incomplete=7, is_transition=True, to_glacier=30, expiration=60,
                        noncurrent_expiration=60):
        bucket.add_lifecycle_rule(
            id="abort-incomplete-multipart-upload",
            abort_incomplete_multipart_upload_after=cdk.Duration.days(incomplete),
            enabled=True
        )
        if is_transition:
            bucket.add_lifecycle_rule(
                id="transitions-to-glacier",
                transitions=[
                    s3.Transition(
                        storage_class=s3.StorageClass.GLACIER,
                        transition_after=cdk.Duration.days(to_glacier)
                    )
                ],
                noncurrent_version_transitions=[
                    s3.NoncurrentVersionTransition(
                        storage_class=s3.StorageClass.GLACIER,
                        transition_after=cdk.Duration.days(to_glacier)
                    )
                ],
                enabled=True
            )
        bucket.add_lifecycle_rule(
            id="expiration",
            expiration=cdk.Duration.days(expiration),
            enabled=True
        )
        bucket.add_lifecycle_rule(
            id="noncurrent-version-expiration",
            noncurrent_version_expiration=cdk.Duration.days(noncurrent_expiration),
            enabled=True
        )
