from aws_cdk import (
    aws_logs as logs,
    core
)

from l3_constructs.kms.L3Key import L3Key
from utils.IAMPrincipals import IAMPrincipals


class L3LogGroup(logs.LogGroup):
    """
        CDK Construct to create a CloudWatch LogGroup
    """

    def __init__(self, scope: core.Construct, id: str,
                 name: str = None,
                 removal_policy: core.RemovalPolicy = None):
        encryption_key = L3Key(
            scope, f'{id}LogsKey',
            name=f'logs/{name or id}'
        )

        super(L3LogGroup, self).__init__(
            scope, id,
            retention=logs.RetentionDays.TWO_WEEKS,
            encryption_key=encryption_key,
            log_group_name=name or None,
            removal_policy=removal_policy or None
        )

        encryption_key.grant_encrypt_decrypt(IAMPrincipals.LOGS.value.grant_principal)
