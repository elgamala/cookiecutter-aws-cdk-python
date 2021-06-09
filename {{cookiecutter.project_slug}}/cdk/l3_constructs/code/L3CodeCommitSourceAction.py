from aws_cdk import (
    aws_codepipeline_actions as cpa,
    aws_codepipeline as cp,
    aws_codecommit as cc,
    aws_iam as iam,
    core
)

from utils.IAMPrincipals import IAMPrincipals


class L3CodeCommitSourceAction(cpa.CodeCommitSourceAction):

    def __init__(self, repository: cc.Repository,
                 action_name: str,
                 pipeline_role: iam.Role):
        self.pipeline_artifact = cp.Artifact()

        self.role = iam.Role(
            core.Stack.of(repository), f'CodePipeline-{repository.node.id}-Role',
            assumed_by=pipeline_role
        )
        pipeline_role.grant(self.role, 'sts:AssumeRole')

        repository.grant_read(self.role)

        super().__init__(
            action_name=action_name,
            variables_namespace=f'{L3CodeCommitSourceAction.__name__}-{action_name}',
            repository=repository,
            branch='master',
            output=self.pipeline_artifact,
            code_build_clone_output=True,
            role=self.role
        )
