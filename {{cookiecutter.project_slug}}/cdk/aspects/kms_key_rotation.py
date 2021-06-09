import jsii
from aws_cdk import (
    core,
    aws_iam as iam
)


@jsii.implements(core.IAspect)
class KMSKeyRotationAspect:

    def visit(self, construct: core.IConstruct) -> None:

        if isinstance(construct, core.CfnResource):
            if construct.cfn_resource_type in ["AWS::KMS::Key"]:
                construct.add_property_override(
                    property_path="EnableKeyRotation",
                    value=True
                )
