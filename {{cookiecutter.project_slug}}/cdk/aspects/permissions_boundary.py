import jsii
from aws_cdk import (
    core,
)

"""
    Aspect class to automatically apply IAM Permissions Boundary
    for any new IAM Principal that gets created by the CDK App.
"""


@jsii.implements(core.IAspect)
class PermissionsBoundaryAspect:
    """
        Constructor to take the AWS account id and Permissions
        boundary IAM Policy name to be able to generate the ARN
    """

    def __init__(self, account: str, policy_name: str):
        self.policy_arn_static = f"arn:aws:iam::{account}:policy/{policy_name}"
        self.policy_arn_dynamic = f"arn:aws:iam::{core.Aws.ACCOUNT_ID}:policy/{policy_name}"

    """
        Visit method is called by CDK while traversing the CDK
        Construct tree so that we have to filter here for the
        relevant apps i.e. IAM Roles and IAM Users to apply
        the Permissions Boundary policy to them.

        In order to apply changes to the resulting CFN resources
        you need to deal with the underlying CFN resource using
        the notation <construct>.node.default_child to set whatever
        Cloud Formation attribute that you want to set.
    """

    def visit(self, construct: core.IConstruct) -> None:

        if isinstance(construct, core.CfnResource):
            if construct.cfn_resource_type in ["AWS::IAM::Role", "AWS::IAM::User"]:
                if "RancherManagementRoleId" in construct.logical_id:
                    # skip for rancher management role
                    pass
                elif "EKSClusterRBACRoles" in construct.logical_id:
                    construct.add_property_override(
                        property_path="PermissionsBoundary",
                        value=self.policy_arn_dynamic
                    )
                else:
                    construct.add_property_override(
                        property_path="PermissionsBoundary",
                        value=self.policy_arn_static
                    )
