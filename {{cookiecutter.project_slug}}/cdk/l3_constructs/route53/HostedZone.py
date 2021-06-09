from aws_cdk import (
    aws_route53 as r53,
    aws_ec2 as ec2,
    core
)

from l3_constructs.logs.L3LogGroup import L3LogGroup


class HostedZone(r53.HostedZone):
    """
       CDK Construct to deploy a new Route53 Hosted Zone with logs enabled
    """

    def __init__(self,
                 scope: core.Construct,
                 id: str,
                 domain_name: str,
                 vpcs: [ec2.Vpc] = None) -> None:

        query_logs_group = L3LogGroup(
            self, f'{id}LogGroup',
            name=f'/aws/route53/{domain_name}'
        )

        super(HostedZone, self).__init__(
            scope=scope,
            id=id,
            zone_name=domain_name,
            vpcs=vpcs or None,
            query_logs_log_group_arn= query_logs_group.log_group_arn
        )
