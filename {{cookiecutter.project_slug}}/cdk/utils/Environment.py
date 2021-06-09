import json
from enum import Enum

from aws_cdk import (
    core
)


def get_environment(env_name: str):
    environments = cdk_json.get('environments')

    return core.Environment(**environments[env_name])


def read_cdk_context_json():
    filename = "cdk.json"

    with open(filename, 'r') as myfile:
        data = myfile.read()

    # parse file
    obj = json.loads(data)

    return obj.get('context')


cdk_json = read_cdk_context_json()


class Environment(Enum):
    TOOLING: core.Environment = get_environment('tooling')
    MASTER: core.Environment = get_environment('master')
    DISASTER_RECOVERY: core.Environment = get_environment('disasterRecovery')
