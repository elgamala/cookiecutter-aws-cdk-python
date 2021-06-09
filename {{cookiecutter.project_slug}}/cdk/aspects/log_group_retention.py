import jsii
from aws_cdk import (
    core,
    aws_logs as logs,
    aws_lambda as lambda_,
)


@jsii.implements(core.IAspect)
class LogGroupRetention:

    def __init__(self, retention_days: logs.RetentionDays):
        super(LogGroupRetention, self).__init__()
        self.retention_days = retention_days
        self.last_name = ''

    def visit(self, construct: core.IConstruct) -> None:
        if construct.node.id != 'framework-onEvent':
            self.last_name = construct.node.id

        id = f'{construct.node.id}LRAspect'
        if construct.node.id == 'framework-onEvent':
            id = f'{self.last_name}{construct.node.id}LRAspect'

        if isinstance(construct, lambda_.Function):
            lambda_.LogRetention(
                scope=core.Stack.of(construct),
                id=id,
                log_group_name=construct.log_group.log_group_name,
                retention=logs.RetentionDays.TWO_WEEKS
            )
