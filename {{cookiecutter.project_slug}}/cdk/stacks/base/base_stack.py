from pathlib import Path
import yaml
from aws_cdk import (
    aws_iam as iam,
    core
)
from git import InvalidGitRepositoryError

from l3_constructs.git.GitCommit import GitCommit
from utils.CDKParams import CDKParams


class BaseStack(core.Stack):

    def __init__(self, scope: core.Construct,
                 env: core.Environment,
                 id: str = None,
                 extra_tags: [core.Tag] = None,
                 config_root: str = None) -> None:
        cdk_helper = CDKParams(scope)
        self.stack_prefix = cdk_helper.stack_prefix
        super().__init__(scope, id or f"{self.stack_prefix}-{type(self).__name__}", **{'env': env})

        try:
            GitCommit(self)
        except InvalidGitRepositoryError:
            print('Warning: Not a git repo, skip adding SSM parameters for GitCommit tracking')

        self.params = cdk_helper.params

        """
           Tagging for the overall stack with extra tags
        """
        core.Tags.of(self).add(
            key="CDK/StackClass",
            value=type(self).__name__
        )
        if config_root:
            core.Tags.of(self).add(
                key=f"CDK/ConfigRoot",
                value=config_root
            )
        if extra_tags:
            for extra_tag in extra_tags:
                core.Tags.of(self).add(**extra_tag)

    def read_file(self, relative_path: str) -> str:
        path = Path(__file__).parent.parent / f"{relative_path}"
        with path.open() as f:
            return f.read()

    def get_iam_role_arn(self, role_name: str) -> str:
        return core.Arn.format(
            stack=self,
            components=core.ArnComponents(
                service="iam",
                partition='aws',
                region='',
                resource="role",
                resource_name=role_name
            )
        )

    def get_iam_role(self, role_name: str):
        return iam.Role.from_role_arn(
            scope=self,
            id=self.generate_random_name(role_name),
            role_arn=self.get_iam_role_arn(role_name)
        )

    def load_manifest(self, file_relative_path):
        path = Path(__file__).parent.parent / f"{file_relative_path}"
        with path.open() as file:
            documents = yaml.full_load(file)

            for item, doc in documents.items():
                print(item, ":", doc)

            return documents
