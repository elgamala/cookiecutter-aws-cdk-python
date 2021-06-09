from enum import Enum

from aws_cdk import (
    core,
    aws_iam as iam
)

from utils.Environment import Environment


class IAMPrincipals(Enum):
    LAMBDA: iam.IPrincipal = iam.ServicePrincipal(service=f'lambda.{core.Aws.URL_SUFFIX}')
    EC2: iam.IPrincipal = iam.ServicePrincipal(service=f'ec2.{core.Aws.URL_SUFFIX}')
    SSM: iam.IPrincipal = iam.ServicePrincipal(service=f'ssm.{core.Aws.URL_SUFFIX}')
    EKS: iam.IPrincipal = iam.ServicePrincipal(service=f'eks.{core.Aws.URL_SUFFIX}')
    S3: iam.IPrincipal = iam.ServicePrincipal(service=f's3.{core.Aws.URL_SUFFIX}')
    SECRETS_MANAGER: iam.IPrincipal = iam.ServicePrincipal(service=f'secretsmanager.{core.Aws.URL_SUFFIX}')
    CODE_BUILD: iam.IPrincipal = iam.ServicePrincipal(service=f'codebuild.{core.Aws.URL_SUFFIX}')
    CODE_PIPELINE: iam.IPrincipal = iam.ServicePrincipal(service=f'codepipeline.{core.Aws.URL_SUFFIX}')
    CLOUD_FORMATION: iam.IPrincipal = iam.ServicePrincipal(service=f'cloudformation.{core.Aws.URL_SUFFIX}')
    ROUTE_53: iam.IPrincipal = iam.ServicePrincipal(service=f'route53.{core.Aws.URL_SUFFIX}')
    LOGS: iam.IPrincipal = iam.ServicePrincipal(service=f'logs.{core.Aws.URL_SUFFIX}')
    BACKUP: iam.IPrincipal = iam.ServicePrincipal(service=f'backup.{core.Aws.URL_SUFFIX}')

    TOOLING_ACCOUNT: iam.IPrincipal = iam.AccountPrincipal(Environment.TOOLING.value.account)
    MASTER_ACCOUNT: iam.IPrincipal = iam.AccountPrincipal(Environment.MASTER.value.account)
    DISASTER_RECOVERY_ACCOUNT: iam.IPrincipal = iam.AccountPrincipal(Environment.DISASTER_RECOVERY.value.account)

    @staticmethod
    def composite_principal(principals: [iam.ServicePrincipal]):
        composite: iam.IPrincipal = iam.CompositePrincipal(*principals)
        return composite

    @staticmethod
    def get_key_admins(scope: core.Construct, id: str):
        kms_config = scope.node.try_get_context('parameters')['kms']
        return IAMPrincipals.get_roles(scope, id, kms_config['keyAdminRoleNames'])

    @staticmethod
    def get_cluster_admins(scope: core.Construct, id: str):
        eks_config = scope.node.try_get_context('parameters')['eks']
        return IAMPrincipals.get_roles(scope, id, eks_config['eksAdminRoleNames'])

    @staticmethod
    def get_role(scope: core.Construct, id: str, role_name: str):
        return iam.Role.from_role_arn(
            scope, f'{id}{role_name}',
            core.Arn.format(
                components=core.ArnComponents(
                    partition='aws',
                    account=core.Stack.of(scope).account,
                    region='',
                    service='iam',
                    resource='role',
                    resource_name=role_name
                ),
                stack=core.Stack.of(scope)
            ))

    @staticmethod
    def get_roles(scope: core.Construct, id: str, role_names: [str]):
        roles = []
        for role_name in role_names:
            roles.append(IAMPrincipals.get_role(scope, id, role_name))
        return roles
