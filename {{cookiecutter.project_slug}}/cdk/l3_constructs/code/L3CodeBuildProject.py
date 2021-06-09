from aws_cdk import (
    aws_codebuild as cb,
    aws_iam as iam,
    aws_s3 as s3,
    core
)


class L3CodeBuildProject(cb.PipelineProject):

    def __init__(self, scope: core.Construct, id: str, build_spec: cb.BuildSpec, cache_bucket: s3.Bucket,  role: iam.Role = None):
        super().__init__(
            scope, id,
            build_spec=build_spec,
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_5_0,
                compute_type=cb.ComputeType.MEDIUM,
                privileged=True
            ),
            cache=cb.Cache.bucket(
                bucket=cache_bucket
            ),
            role=role
        )
