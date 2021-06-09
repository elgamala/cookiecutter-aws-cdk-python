import jsii
from aws_cdk import (
    core,
)


@jsii.implements(core.IAspect)
class RetainKubernetesResources:

    def visit(self, construct: core.IConstruct) -> None:

        if isinstance(construct, core.CfnResource):
            if construct.cfn_resource_type in ['Custom::AWSCDK-EKS-KubernetesResource']:
                construct.add_override('DeletionPolicy',core.RemovalPolicy.RETAIN.value.title())
