from aws_cdk import (
    aws_kms as kms,
    core
)

from utils.IAMPrincipals import IAMPrincipals


class L3Key(kms.Key):
    """
        CDK Construct to create a KMS Key
    """

    def __init__(self, scope: core.Construct, id: str,
                 name: str = None,
                 description: str = None,
                 removal_policy: core.RemovalPolicy = None):
        super(L3Key, self).__init__(
            scope, id,
            admins=IAMPrincipals.get_key_admins(scope, id),
            enable_key_rotation=True,
            enabled=True,
            description=description or None,
            removal_policy= removal_policy or core.RemovalPolicy.DESTROY,
            alias=f'{name or id}'.replace(".", "-")
        )
