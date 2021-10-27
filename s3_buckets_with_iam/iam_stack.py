from aws_cdk import (
    aws_iam as iam,
    aws_s3 as s3,
    core as cdk
)


class IAMStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, to_casmart: s3.Bucket, to_thermofisher: s3.Bucket,
                 config_db: s3.Bucket, logs: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        thermofisher_group = iam.Group(self, construct_id + "tmogroup", group_name=construct_id + '-thermofisher')
        thermofisher_policy = iam.ManagedPolicy(self, construct_id + "tmopolicy",
                                                managed_policy_name=construct_id + '-thermofisher',
                                                description='The policy controls who can access B2B Marketplace S3 buckets on the ThermoFisher side.',
                                                statements=[
                                                    iam.PolicyStatement(
                                                        sid='AllowUserToSeeBucketListInTheConsole',
                                                        actions=['s3:ListAllMyBuckets', 's3:GetBucketLocation'],
                                                        resources=['arn:aws-cn:s3:::*']
                                                    ),
                                                    iam.PolicyStatement(
                                                        sid='AllowListingOfSpecificBucket',
                                                        actions=['s3:GetBucketLocation', 's3:ListBucket'],
                                                        resources=[
                                                            'arn:aws-cn:s3:::' + to_casmart.bucket_name,
                                                            'arn:aws-cn:s3:::' + to_casmart.bucket_name + '/*',
                                                            'arn:aws-cn:s3:::' + to_thermofisher.bucket_name,
                                                            'arn:aws-cn:s3:::' + to_thermofisher.bucket_name + '/*',
                                                            'arn:aws-cn:s3:::' + config_db.bucket_name,
                                                            'arn:aws-cn:s3:::' + config_db.bucket_name + '/*',
                                                            'arn:aws-cn:s3:::' + logs.bucket_name,
                                                            'arn:aws-cn:s3:::' + logs.bucket_name + '/*'
                                                        ]
                                                    ),
                                                    iam.PolicyStatement(
                                                        sid='AllowGetObjectOfSpecificBucket',
                                                        actions=['s3:GetObject'],
                                                        resources=[
                                                            'arn:aws-cn:s3:::' + to_thermofisher.bucket_name,
                                                            'arn:aws-cn:s3:::' + to_thermofisher.bucket_name + '/*'
                                                        ]
                                                    ),
                                                    iam.PolicyStatement(
                                                        sid='AllowPutObjectOfSpecificBucket',
                                                        actions=['s3:PutObject'],
                                                        resources=[
                                                            'arn:aws-cn:s3:::' + to_casmart.bucket_name,
                                                            'arn:aws-cn:s3:::' + to_casmart.bucket_name + '/*',
                                                            'arn:aws-cn:s3:::' + config_db.bucket_name,
                                                            'arn:aws-cn:s3:::' + config_db.bucket_name + '/*',
                                                            'arn:aws-cn:s3:::' + logs.bucket_name,
                                                            'arn:aws-cn:s3:::' + logs.bucket_name + '/*'
                                                        ]
                                                    )
                                                ]
                                                )
        thermofisher_group.add_managed_policy(thermofisher_policy)
        thermofisher_user = iam.User(self, construct_id + 'tmouser', user_name=construct_id + '-thermofisher-api-user',
                                     groups=[thermofisher_group])
        thermofisher_user_key = iam.CfnAccessKey(self, construct_id + 'tmouserkey',
                                                 user_name=thermofisher_user.user_name)

        cdk.CfnOutput(self, construct_id + 'outtmouser', export_name='ThermoFisherUsername',
                      value=thermofisher_user.user_name)
        cdk.CfnOutput(self, construct_id + 'outtmouseraccess', export_name='ThermoFisherAccessKeyId',
                      value=thermofisher_user_key.ref)
        cdk.CfnOutput(self, construct_id + 'outtmousersecret', export_name='ThermoFisherSecretAccessKey',
                      value=thermofisher_user_key.attr_secret_access_key)

        casmart_group = iam.Group(self, construct_id + "casgroup", group_name=construct_id + '-casmart')
        casmart_policy = iam.ManagedPolicy(self, construct_id + "caspolicy",
                                           managed_policy_name=construct_id + '-casmart',
                                           description='The policy controls who can access B2B Marketplace S3 buckets on the Casmart side.',
                                           statements=[
                                               iam.PolicyStatement(
                                                   sid='AllowUserToSeeBucketListInTheConsole',
                                                   actions=['s3:ListAllMyBuckets', 's3:GetBucketLocation'],
                                                   resources=['arn:aws-cn:s3:::*']
                                               ),
                                               iam.PolicyStatement(
                                                   sid='AllowListingOfSpecificBucket',
                                                   actions=['s3:GetBucketLocation', 's3:ListBucket'],
                                                   resources=[
                                                       'arn:aws-cn:s3:::' + to_casmart.bucket_name,
                                                       'arn:aws-cn:s3:::' + to_casmart.bucket_name + '/*',
                                                       'arn:aws-cn:s3:::' + to_thermofisher.bucket_name,
                                                       'arn:aws-cn:s3:::' + to_thermofisher.bucket_name + '/*'
                                                   ]
                                               ),
                                               iam.PolicyStatement(
                                                   sid='AllowGetObjectOfSpecificBucket',
                                                   actions=['s3:GetObject'],
                                                   resources=[
                                                       'arn:aws-cn:s3:::' + to_casmart.bucket_name,
                                                       'arn:aws-cn:s3:::' + to_casmart.bucket_name + '/*'
                                                   ]
                                               ),
                                               iam.PolicyStatement(
                                                   sid='AllowPutObjectOfSpecificBucket',
                                                   actions=['s3:PutObject'],
                                                   resources=[
                                                       'arn:aws-cn:s3:::' + to_thermofisher.bucket_name,
                                                       'arn:aws-cn:s3:::' + to_thermofisher.bucket_name + '/*'
                                                   ]
                                               )
                                           ]
                                           )
        casmart_group.add_managed_policy(casmart_policy)
        casmart_user = iam.User(self, construct_id + 'casuser', user_name=construct_id + '-casmart-api-user',
                                groups=[casmart_group])

        casmart_user_key = iam.CfnAccessKey(self, construct_id + 'casuserkey',
                                            user_name=casmart_user.user_name)

        cdk.CfnOutput(self, construct_id + 'outcasuser', export_name='CasmartUsername',
                      value=casmart_user.user_name)
        cdk.CfnOutput(self, construct_id + 'outcasuseraccess', export_name='CasmartAccessKeyId',
                      value=casmart_user_key.ref)
        cdk.CfnOutput(self, construct_id + 'outcasusersecret', export_name='CasmartSecretAccessKey',
                      value=casmart_user_key.attr_secret_access_key)
