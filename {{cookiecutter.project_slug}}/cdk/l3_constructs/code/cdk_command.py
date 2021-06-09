from enum import Enum

from aws_cdk.aws_codebuild import BuildSpec


class CdkCommand(Enum):
    BOOTSTRAP = "bootstrap"
    TEST = "test"
    SECURITY_CHECKS = "security-checks"
    DIFF = "diff"
    DEPLOY = "deploy"


def from_cdk_command(command: CdkCommand):
    return BuildSpec.from_object({
        'version': 0.2,
        'phases': {
            'install': {
                'runtime-versions': {
                    'python': '3.9',
                    'nodejs': '14'
                },
                'commands': [
                    'chmod +x ./cdk/l3_constructs/code/install_commands.sh',
                    './cdk/l3_constructs/code/install_commands.sh'
                ]
            },
            'build': {
                'commands': [
                    f'make {command.value}'
                ]
            }
        },
        "cache": {
            "paths": [
                "/root/cache/**/*",
            ]
        }
    })
