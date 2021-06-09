from aws_cdk import (
    aws_iam as iam,
    aws_eks as eks,
    core
)
from pathlib import Path

import yaml


class BaseNestedStack(core.NestedStack):
    stack_prefix = "{{ cookiecutter.project_name }}"

    def __init__(self, scope: core.Construct, id: str = None, extra_tags: [core.Tag] = None, config_root: str = None,
                 **kwargs) -> None:
        super().__init__(scope, id or f"{self.stack_prefix}-{type(self).__name__}")

        self.params = scope.params

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
        return self.get_arn("iam", "role", role_name)

    def get_secret_arn(self, secret_name: str) -> str:
        return self.get_arn("secretsmanager", "secret", secret_name)

    def get_arn(self, service, resource, resource_name: str) -> str:
        return core.Arn.format(
            stack=self,
            components=core.ArnComponents(
                service=service,
                resource=resource,
                resource_name=resource_name
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
