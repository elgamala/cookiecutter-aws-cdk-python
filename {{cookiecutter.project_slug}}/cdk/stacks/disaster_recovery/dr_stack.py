from aws_cdk import (
    core,
    aws_kms as kms
)

from l3_constructs.kms.KmsLookup import KmsLookup
from stacks.base.base_stack import BaseStack
from utils.CDKParams import CDKParams
from utils.Environment import Environment


class DrStack(BaseStack):

    def __init__(self, scope: core.Construct,
                 original_scope: core.Construct,
                 env: core.Environment,
                 id: str = None):
        self.original_scope = original_scope
        super(DrStack, self).__init__(
            scope=scope, id=id, env=env
        )

    def lookup_kms_key(self, key_alias: str) -> kms.Key:
        key_lookup = KmsLookup(
            original_scope=self.original_scope,
            dr_scope=self,
            id=f'KmsLookup/{key_alias}',
            key_alias=key_alias)

        return kms.Key.from_key_arn(
            scope=self.original_scope,
            id=f'LookedUpKmsKey{key_alias}',
            key_arn=key_lookup.kms_key_arn
        )

    @staticmethod
    def of(scope: core.Construct, id: str):
        return DrStack(
            core.App.of(scope),
            original_scope=scope,
            id=f'{CDKParams().stack_prefix}-DR-{id}',
            env=Environment.DISASTER_RECOVERY.value
        )
