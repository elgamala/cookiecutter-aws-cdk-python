import jsii
from aws_cdk import (
    core,
    aws_ec2 as ec2
)


@jsii.implements(core.IAspect)
class EBSVolumeKMSEncryption:

    def visit(self, construct: core.IConstruct) -> None:

        if isinstance(construct, ec2.Instance):
            resource: core.CfnResource = construct.node.default_child
            resource.add_property_override(
                property_path="BlockDeviceMappings.0.Ebs.Encrypted",
                value=True
            )

        if isinstance(construct, ec2.LaunchTemplate):
            resource: core.CfnResource = construct.node.default_child
            resource.add_property_override(
                property_path='LaunchTemplateData.BlockDeviceMappings.0.Ebs.Encrypted',
                value=True
            )
