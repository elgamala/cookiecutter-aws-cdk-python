import json
from aws_cdk import core
from aws_cdk.aws_logs import RetentionDays
from aws_cdk.core import Tags, Aspects

from aspects.ebs_volume_kms_encryption import EBSVolumeKMSEncryption
from aspects.kms_key_rotation import KMSKeyRotationAspect
from aspects.log_group_retention import LogGroupRetention
from aspects.s3_bucket_kms_encryption import S3BucketKMSEncryption
from utils.CDKParams import CDKParams


class BaseApp(core.App):
    cdk_params = CDKParams()
    stack_prefix = cdk_params.stack_prefix

    def __init__(self):
        super().__init__()

        print(f'Environments= {json.dumps( self.node.try_get_context("environments"), indent=4)}')

        self.params = self.node.try_get_context('parameters')

        tags: [
            {
                "key": str,
                "value": str
            }
        ] = self.params.get('all').get('tags')

        for tag in tags:
            Tags.of(self).add(**tag)

        Tags.of(self).add(key='Project', value=self.cdk_params.stack_prefix)

        Aspects.of(self).add(
            S3BucketKMSEncryption()
        )

        Aspects.of(self).add(
            KMSKeyRotationAspect()
        )

        Aspects.of(self).add(
            EBSVolumeKMSEncryption()
        )

        Aspects.of(self).add(
            LogGroupRetention(RetentionDays.TWO_WEEKS)
        )

    def read_cdk_context_json(self):
        filename = "cdk.context.json"

        with open(filename, 'r') as myfile:
            data = myfile.read()

        obj = json.loads(data)

        return obj.get('context')

    def stack_name(self, stack_name: str) -> str:
        return f"{self.stack_prefix}-{stack_name}"
