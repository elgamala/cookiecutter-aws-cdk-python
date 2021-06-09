from aws_cdk import (
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_secretsmanager as sm,
    custom_resources as cr,
    core
)


class SecretReader(lambda_.Function):
    prefix = 'EcoStruxure'

    def __init__(
            self, scope: core.Construct, id: str,
            secret: sm.Secret,
            attribute_name: str = None) -> None:
        super(SecretReader, self).__init__(
            scope=scope,
            id=id,
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset('./cdk/l3_constructs/secrets_manager/SecretReaderCR'),
            handler='index.handler'
        )

        self.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'secretsmanager:DescribeSecret',
                'secretsmanager:GetSecretValue',
                'secretsmanager:RotateSecret',
                'secretsmanager:UpdateSecretVersionStage',
                'secretsmanager:PutSecretValue'
            ],
            resources=[secret.secret_arn]
        ))

        self.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                'kms:Decrypt'
            ],
            resources=['*']
        ))

        provider = cr.Provider(
            self, f'{id}Provider',
            on_event_handler=self
        )

        custom_resource = core.CustomResource(
            self, f'{id}CR',
            service_token=provider.service_token,
            properties={
                "SecretArn": secret.secret_arn,
                "AttributeName": attribute_name or None
            }
        )

        self.secret_value = custom_resource.get_att_string('SecretValue')
