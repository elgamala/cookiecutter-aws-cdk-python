from aws_cdk import (
    aws_codecommit as codecommit,
    core
)

from stacks.base.base_stack import BaseStack


class CodeCommit(BaseStack):

    def __init__(self, scope: core.Construct, id: str,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        repo_name = self.params.get('codeCommit')

        # create repository
        self.repo = codecommit.Repository(
            scope=self,
            id=f"{repo_name}",
            repository_name=repo_name,
        )

        resource: core.CfnResource = self.repo.node.find_child('Resource')
        resource.deletion_policy = core.CfnDeletionPolicy.RETAIN.value

