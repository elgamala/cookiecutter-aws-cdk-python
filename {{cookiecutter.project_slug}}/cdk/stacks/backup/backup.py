from aws_cdk import (
    aws_events as events,
    aws_backup as backup,
    aws_iam as iam,
    core
)

from l3_constructs.kms.L3Key import L3Key
from stacks.base.base_stack import BaseStack
from stacks.disaster_recovery.dr_stack import DrStack
from utils.IAMPrincipals import IAMPrincipals


class BackupStack(BaseStack):
    """
        Constructor that Deploys AWS Backup plan
    """

    def __init__(self,
                 scope: core.Construct,
                 env: core.Environment,
                 id: str = None) -> None:
        super().__init__(scope=scope, id=id, env=env)

        dr_stack = DrStack.of(self, BackupStack.__name__)

        vault_name = f'{self.stack_prefix}-BackupVault'
        vault_key_alias = 'backup/Vault'

        local_key = L3Key(
            self, vault_key_alias
        )

        local_vault = backup.BackupVault(
            self, vault_name,
            backup_vault_name=vault_name,
            encryption_key=local_key
        )

        dr_key = L3Key(
            dr_stack, vault_key_alias,
            name=vault_name
        )

        dr_vault = backup.BackupVault(
            dr_stack, vault_name,
            backup_vault_name=vault_name,
            encryption_key=dr_key
        )

        plan = backup.BackupPlan.daily_monthly1_year_retention(
            self, f'{self.stack_prefix}-BackupPlan',
            backup_vault=local_vault
        )

        role = iam.Role(
            dr_stack, 'Role',
            role_name=core.PhysicalName.GENERATE_IF_NEEDED,
            assumed_by=IAMPrincipals.BACKUP.value
        )

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
            'service-role/AWSBackupServiceRolePolicyForBackup'
        ))

        dr_key.grant_encrypt_decrypt(role)

        plan.add_selection(
            'AllEBSVolumes',
            role=role,
            resources=[
                backup.BackupResource.from_tag(
                    key='Project',
                    value=self.stack_prefix
                )
            ]
        )

        resource: core.CfnResource = plan.node.default_child
        resource.add_property_override(
            'BackupPlan.BackupPlanRule.0.CopyActions', [
                {'DestinationBackupVaultArn': core.Arn.format(
                    core.ArnComponents(
                        partition=core.Aws.PARTITION,
                        account=dr_stack.account,
                        region=dr_stack.region,
                        service='backup',
                        resource='backup-vault',
                        resource_name=vault_name,
                        sep=":"
                    ),
                    stack=self
                )}
            ]
        )

        self.node.add_dependency(dr_stack)

