from apps.base_app import BaseApp
from stacks.backup.backup import BackupStack
from stacks.pipeline.pipeline import CICDPipeline
from utils.Environment import Environment


class IacApp(BaseApp):

    def __init__(self):
        super(IacApp, self).__init__()

        self.cicd_pipeline = CICDPipeline(
            scope=self,
            env=Environment.TOOLING.value
        )

        self.backup = BackupStack(
            scope=self,
            env=Environment.MASTER.value
        )

        self.synth()
