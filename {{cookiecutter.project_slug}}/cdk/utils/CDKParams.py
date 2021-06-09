import pkg_resources
from aws_cdk import (
    core
)


class CDKParams:

    def __init__(self, scope: core.Construct = None):
        self.stack_prefix = "{{ cookiecutter.project_name }}"
        self.version = '1.0.0'
        self.cdk_version = cdk_version = pkg_resources.require("aws-cdk.core")[0].version

        if scope:
            self.params = scope.node.try_get_context('parameters')

