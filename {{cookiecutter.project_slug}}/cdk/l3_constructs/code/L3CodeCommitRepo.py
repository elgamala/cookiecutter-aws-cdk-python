from aws_cdk import (
    core,
    aws_codecommit as cc
)


class CodeCommitRepo(cc.Repository):

    def __init__(self, scope: core.Construct, id: str, repository_name: str, description: str = None):
        super().__init__(
            scope, id,
            repository_name=repository_name,
            description=description
        )
        cfn_resource = self.node.findChild('Resource')
        if isinstance(cfn_resource, core.CfnResource):
            cfn_resource.add_override('DeletionPolicy', core.RemovalPolicy.RETAIN.value.title())
