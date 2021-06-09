from aws_cdk import (
    aws_iam as iam,
    core
)
from pathlib import Path
import yaml


class BaseConstruct(core.Construct):

    stack_prefix = "{{ cookiecutter.project_name }}"

    def __init__(self, scope: core.Construct, id: str = None, extra_tags: [core.Tag] = None, config_root: str = None,
                 **kwargs) -> None:
        super().__init__(scope, id or f"{self.stack_prefix}-{type(self).__name__}")

        self.params = scope.params

        if extra_tags:
            for extra_tag in extra_tags:
                core.Tags.of(self).add(**extra_tag)

    def read_file(self, relative_path: str) -> str:
        path = Path(__file__).parent.parent / f"{relative_path}"
        with path.open() as f:
            return f.read()

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
