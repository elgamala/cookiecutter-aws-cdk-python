from aws_cdk import (

    aws_iam as iam,
    aws_lambda as lambda_,
    custom_resources as cr,
    core
)

from utils.IAMPrincipals import IAMPrincipals


class KmsLookup(lambda_.SingletonFunction):

    def __init__(self, original_scope: core.Construct, dr_scope: core.Construct, id: str, key_alias: str):
        role = iam.Role(
            dr_scope, f'{id}KMSLookUpRole',
            role_name=core.PhysicalName.GENERATE_IF_NEEDED,
            assumed_by=IAMPrincipals.EKS_MASTER_ACCOUNT.value
        )

        role.add_to_policy(iam.PolicyStatement(
            actions=['kms:DescribeKey'],
            resources=['*']
        ))

        super(KmsLookup, self).__init__(
            scope=original_scope,
            id=id,
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('./cdk/l3_constructs/kms/KmsLookupLambda'),
            handler='__init__.lambda_handler',
            uuid='KmsLookupLambda',
            environment={
                "AwsAccountId": core.Stack.of(dr_scope).account,
                "AwsRegion": core.Stack.of(dr_scope).region,
                "RoleName": role.role_name
            }
        )

        self.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'sts:AssumeRole'
            ],
            resources=[role.role_arn]
        ))

        cr_provider = cr.Provider(
            self, f'{id}CRP',
            on_event_handler=self
        )

        get_kms_key_id = core.CustomResource(
            self, f'{id}GetKmsKeyIdByAlias',
            service_token=cr_provider.service_token,
            properties={
                "KmsAlias": key_alias
            }
        )

        self.kms_key_arn = get_kms_key_id.get_att_string('Arn')
