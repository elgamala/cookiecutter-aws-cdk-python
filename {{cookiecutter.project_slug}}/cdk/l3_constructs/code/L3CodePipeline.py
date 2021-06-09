from aws_cdk import (
    core,
    aws_codepipeline as cp
)

from l3_constructs.s3.L3Bucket import L3Bucket


class L3CodePipeline(cp.Pipeline):

    def __init__(self, scope: core.Construct, id: str, pipeline_name: str):

        artifact_bucket = L3Bucket(
            scope, f'{id}ArtifactBucket'
        )

        super().__init__(
            scope, id,
            pipeline_name=pipeline_name,
            restart_execution_on_update=True,
            cross_account_keys=True,
            artifact_bucket=artifact_bucket
        )

