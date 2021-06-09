from aws_cdk import (
    aws_secretsmanager as sm,
    aws_iam as iam,
    core
)
from l3_constructs.kms.L3Key import L3Key
from stacks.disaster_recovery.dr_stack import DrStack
from utils.CDKParams import CDKParams


class L3BaseSecret(sm.Secret):

    def __init__(
            self, scope: core.Construct, id: str,
            generate_secret_string: sm.SecretStringGenerator,
            secret_name: str = None) -> None:
        self.config = config = CDKParams(scope)

        full_secret_name = secret_name or id
        if not full_secret_name.startswith('/'):
            full_secret_name = f'/{full_secret_name}'

        self.full_secret_name = f"{config.stack_prefix}{full_secret_name}"

        kms_key_alias = f'secrets{full_secret_name}'

        dr_stack = DrStack.of(scope, id)

        encryption_key = L3Key(
            scope,
            f'{id}SecretsKey',
            name=kms_key_alias
        )

        dr_encryption_key = L3Key(
            dr_stack,
            f'{id}SecretsKey',
            name=kms_key_alias
        )

        dr_encryption_key.grant_decrypt(iam.AccountPrincipal(core.Stack.of(scope).account))

        dr_encryption_key.grant_encrypt_decrypt(iam.AccountPrincipal(dr_stack.account).with_conditions(
            {
                "StringLike": {
                    "kms:ViaService": f'secretsmanager.*.{core.Aws.URL_SUFFIX}'
                }
            }
        ))

        super(L3BaseSecret, self).__init__(
            scope=scope,
            id=id,
            generate_secret_string=generate_secret_string,
            secret_name=f"{config.stack_prefix}{full_secret_name}",
            encryption_key=encryption_key,
            replica_regions=[
                sm.ReplicaRegion(
                    region=dr_stack.region,
                    encryption_key=dr_stack.lookup_kms_key(
                        key_alias=kms_key_alias
                    )
                )
            ]
        )
