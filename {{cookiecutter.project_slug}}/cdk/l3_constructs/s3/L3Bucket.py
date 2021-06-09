from aws_cdk import (
    aws_s3 as s3,
    aws_kms as kms,
    core,
)


class L3Bucket(s3.Bucket):
    def __init__(self, scope: core.Construct, id: str, name: str = None, encryption_key: kms.Key = None):
        if encryption_key:
            encryption = s3.BucketEncryption.KMS
        else:
            encryption = s3.BucketEncryption.KMS_MANAGED
        super(L3Bucket, self).__init__(
            scope, id,
            bucket_name=name or None,
            encryption=encryption,
            encryption_key=encryption_key or None,
            enforce_ssl=True,
            removal_policy=core.RemovalPolicy.RETAIN,
            public_read_access=False,
            auto_delete_objects=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )
