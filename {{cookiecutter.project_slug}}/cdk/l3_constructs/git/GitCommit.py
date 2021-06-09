import json
import os
import socket
from datetime import datetime
import git
from aws_cdk import (
    core,
    aws_ssm as ssm
)

from utils.CDKParams import CDKParams


class GitInfo(object):
    repo_name: str
    repo_branch: str
    commit_sha: str
    commit_message: str
    author_name: str
    author_email: str
    timestamp: str
    host_name: str
    cdk_version: str

    def __init__(self, params: CDKParams = None):
        repo = git.Repo(os.getcwd())

        self.repo_name = repo.remotes.origin.url
        self.repo_branch = 'master'
        self.commit_sha = repo.head.commit.hexsha
        self.commit_message = repo.head.commit.message.replace('\n', '')
        self.author_name = repo.head.commit.author.name.replace('\n', '')
        self.author_email = repo.head.commit.author.email.replace('\n', '')
        self.timestamp = str(repo.head.commit.committed_date)
        self.host_name = socket.gethostname()
        self.timestamp = datetime.fromtimestamp(float(self.timestamp)).isoformat().replace(':', '_')
        if params:
            self.cdk_version = params.cdk_version

    @staticmethod
    def get_prefix():
        return 'CDK/Git'

    def __str__(self):
        return json.dumps(self.__dict__, indent=4)

    def __repr__(self):
        return self.__str__()


class GitCommit(ssm.CfnParameter):
    """
       Placeholder CDK Construct to track which git commit is being deployed using metadata, tags and parameter store
    """

    def __init__(self, scope: core.Construct) -> None:
        _params = CDKParams(scope)

        git_info = GitInfo(_params)

        root_parameter_name = f'/{_params.stack_prefix}/CICD/{scope.node.id}'

        super(GitCommit, self).__init__(
            scope=scope,
            id=root_parameter_name,
            name=root_parameter_name,
            type='String',
            value=scope.node.id
        )

        commit_dict = git_info.__dict__

        param_names = ['CURRENT']

        for param_name in param_names:
            for key in commit_dict.keys():

                parameter_name = f'{root_parameter_name}/Commit/{param_name}/{key.title().replace("_","")}'

                ssm.CfnParameter(
                    scope=scope,
                    id=parameter_name,
                    name=parameter_name,
                    type='String',
                    value=commit_dict[key]
                )

        core.Stack.of(self).template_options.metadata = {
            git_info.get_prefix(): commit_dict
        }

        for tag in commit_dict.keys():
            core.Tags.of(self).add(f'{git_info.get_prefix()}/{tag}', commit_dict[tag])


