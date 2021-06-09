from aws_cdk import (
    aws_route53 as r53,
    core
)


class CNAME(r53.CnameRecord):
    """
       CDK Construct to create a new Route53 CNAME Record into an existing Hosted Zone
    """

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 record_name: str,
                 pointing_to: str,
                 hosted_zone: r53.HostedZone,
                 comment: str = None) -> None:
        super(CNAME, self).__init__(
            scope=scope,
            id=id,
            zone=hosted_zone,
            domain_name=pointing_to,
            record_name=record_name,
            comment=comment
        )
