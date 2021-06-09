import jsii
from aws_cdk import (
    core,
)

"""
    Aspect class to automatically apply S3 bucket encryption AWS:KMS
    for any new S3 Bucket that gets created by the CDK App.
"""


@jsii.implements(core.IAspect)
class S3BucketKMSEncryption:

    """
        Constructor for the Aspect class
    """
    def __init__(self):
        super(S3BucketKMSEncryption, self).__init__()
    """
        Visit method is called by CDK while traversing the CDK
        Construct tree so that we have to filter here for the
        relevant constructs

        In order to apply changes to the resulting CFN resources
        you need to deal with the underlying CFN resource using
        the notation <construct>.node.default_child to set whatever
        Cloud Formation attribute that you want to set.
    """
    def visit(self, construct: core.IConstruct) -> None:
        if isinstance(construct, core.CfnResource):
            if construct.cfn_resource_type == "AWS:S3:Bucket":
                construct.add_property_override(
                    property_path="BucketEncryption.ServerSideEncryptionConfiguration.SSEAlgorithm",
                    value="aws:kms"
                )


