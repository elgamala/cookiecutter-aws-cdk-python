from aws_cdk import (
    aws_codepipeline_actions as cpa,
    aws_codecommit as cc,
    aws_iam as iam,
    aws_secretsmanager as sm,
    core
)

from l3_constructs.code.cdk_command import CdkCommand, from_cdk_command
from l3_constructs.code.L3CodeBuildProject import L3CodeBuildProject
from l3_constructs.code.L3CodeCommitSourceAction import L3CodeCommitSourceAction
from l3_constructs.code.L3CodePipeline import L3CodePipeline
from l3_constructs.s3.L3Bucket import L3Bucket
from stacks.base.base_stack import BaseStack
from utils.Environment import Environment


class CICDPipeline(BaseStack):

    def __init__(
            self,
            scope: core.Construct,
            env: core.Environment,
            id: str = None
    ) -> None:
        super().__init__(scope, id=id, env=env)

        config = self.params.get('cicdPipeline')

        repo_name = self.params.get('codeCommit')

        cache_bucket = L3Bucket(
            self, 'CacheBucket'
        )

        # create repository
        self.repo = cc.Repository(
            scope=self,
            id=f"{repo_name}",
            repository_name=repo_name,
        )
        self.repo.apply_removal_policy(core.RemovalPolicy.RETAIN)

        # CDK CodePipeline
        pipeline = L3CodePipeline(self, 'CodePipeline', f"{self.stack_prefix}-CDKPipeline")
        role = iam.Role(
            self, 'Role',
            assumed_by=iam.ServicePrincipal(f'codebuild.{core.Aws.URL_SUFFIX}'),
        )

        self.repo.grant_read(role)

        statements = [
            iam.PolicyStatement(
                actions=[
                    "cloudformation:*",
                    "route53:*",
                    "sts:*",
                    "ec2:*",
                    "ssm:*",
                    "codecommit:*"
                ],
                resources=[
                    '*'
                ]
            ),
            iam.PolicyStatement(
                actions=[
                    "iam:PassRole"
                ],
                resources=[
                    f'arn:{core.Aws.PARTITION}:iam::{self.account}:role/'
                    f'cdk-{self.node.try_get_context("@aws-cdk/core:bootstrapQualifier")}-'
                    f'cfn-exec-role-{self.account}-{self.region}',

                    f'arn:{core.Aws.PARTITION}:iam::{Environment.DISASTER_RECOVERY.value.account}:role/'
                    f'cdk-{self.node.try_get_context("@aws-cdk/core:bootstrapQualifier")}-'
                    f'cfn-exec-role-{Environment.DISASTER_RECOVERY.value.account}-{Environment.DISASTER_RECOVERY.value.region}'

                ]
            ),
            iam.PolicyStatement(
                actions=[
                    "iam:PutRolePolicy",
                    "iam:GetRole",
                    "iam:GetRolePolicy",
                    "iam:DetachRolePolicy",
                ],
                resources=[
                    '*'
                ]
            )
        ]
        for statement in statements:
            role.add_to_policy(statement)

        # Allow access to the cache bucket and underlying KMS key
        cache_bucket.grant_read_write(role)

        # CDK Source CodeCommit
        cdk_source = L3CodeCommitSourceAction(action_name='SourceAction', repository=self.repo, pipeline_role=pipeline.role)

        test = L3CodeBuildProject(self, 'test', from_cdk_command(CdkCommand.TEST), cache_bucket, role)

        cdk_test_action = cpa.CodeBuildAction(
            action_name='CDK-Test',
            project=test,
            input=cdk_source.pipeline_artifact,
            run_order=1,

        )

        # Diff action
        diff = L3CodeBuildProject(self, 'diff', from_cdk_command(CdkCommand.DIFF), cache_bucket, role)

        cdk_diff_action = cpa.CodeBuildAction(
            action_name='CDK-Diff',
            project=diff,
            input=cdk_source.pipeline_artifact,
            run_order=1,

        )

        # Manual review and approval
        manual_approval = cpa.ManualApprovalAction(
            action_name='Manual-Approval',
            run_order=3
        )

        # Bootstrap action
        bootstrap = L3CodeBuildProject(self, 'bootstrap', from_cdk_command(CdkCommand.BOOTSTRAP), cache_bucket, role)

        cdk_bootstrap_action = cpa.CodeBuildAction(
            action_name='CDK-Bootstrap',
            project=bootstrap,
            input=cdk_source.pipeline_artifact,
            run_order=1,
        )

        # Security Checks action
        security_checks = L3CodeBuildProject(self, 'SecurityChecks', from_cdk_command(CdkCommand.SECURITY_CHECKS), cache_bucket, role)

        security_checks_action = cpa.CodeBuildAction(
            action_name='CDK-SecurityChecks',
            project=security_checks,
            input=cdk_source.pipeline_artifact,
            run_order=1,
        )

        # Deploy action
        deploy = L3CodeBuildProject(self, 'deploy', from_cdk_command(CdkCommand.DEPLOY), cache_bucket, role)

        cdk_deploy_action = cpa.CodeBuildAction(
            action_name='CDK-Deploy',
            project=deploy,
            input=cdk_source.pipeline_artifact,
            run_order=1,
        )

        # Setup the stages
        pipeline.add_stage(
            stage_name='Source',
            actions=[cdk_source]
        )

        pipeline.add_stage(
            stage_name='CDK-Tests',
            actions=[cdk_test_action]
        )

        pipeline.add_stage(
            stage_name='Security-Checks',
            actions=[security_checks_action]
        )

        pipeline.add_stage(
            stage_name='CDK-Diff',
            actions=[cdk_diff_action]
        )

        if 'addManualApprovalStep' in config and config['addManualApprovalStep']:
            pipeline.add_stage(
                stage_name='Manual-Approval',
                actions=[manual_approval],
            )

        pipeline.add_stage(
            stage_name='CDK-Bootstrap',
            actions=[cdk_bootstrap_action]
        )

        pipeline.add_stage(
            stage_name='CDK-Deploy',
            actions=[cdk_deploy_action],
        )
