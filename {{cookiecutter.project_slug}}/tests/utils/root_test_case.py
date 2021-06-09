import json
import re
import typing
from unittest import TestCase

from expects import expect

from cdk_expects_matcher.CdkMatchers import have_resource, ANY_VALUE
import pytest
import json
import os
import fnmatch

cdk_out_dir = 'cdk.out'
stack_prefix = '{{ cookiecutter.project_name }}'
suffix = 'template.json'


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def read(file_path):
    with open(file_path, 'r') as file:
        cfn_template = json.loads(file.read())
        file.close()

    return cfn_template


@pytest.fixture(scope="session")
def synth(request):
    os.system('rm -rf ./cdk.out/')
    os.system('cdk synth --json')


class RootTestCase(TestCase):
    cfn_template = {}  # This is to be injected by a fixture

    secret = 'AWS::SecretsManager::Secret'
    kms_alias = 'AWS::KMS::Alias'
    kms_key = 'AWS::KMS::Key'
    lambda_ = 'AWS::Lambda::Function'
    asg = 'AWS::AutoScaling::AutoScalingGroup'
    asg_lc = 'AWS::AutoScaling::LaunchConfiguration'
    eks_cluster = 'Custom::AWSCDK-EKS-Cluster'
    eks_node_group = 'AWS::EKS::Nodegroup'
    eks_openid_connect_provider = 'Custom::AWSCDKOpenIdConnectProvider'
    iam_role = 'AWS::IAM::Role'
    iam_user = 'AWS::IAM::User'
    iam_group = 'AWS::IAM::Group'
    iam_managed_policy = 'AWS::IAM::ManagedPolicy'
    eks_k8s_manifest = 'Custom::AWSCDK-EKS-KubernetesResource'
    eks_k8s_patch = 'Custom::AWSCDK-EKS-KubernetesPatch'
    s3_bucket = 'AWS::S3::Bucket'
    s3_bucket_policy = 'AWS::S3::BucketPolicy'
    vpc_endpoint = 'AWS::EC2::VPCEndpoint'
    vpc_cidr_block = 'AWS::EC2::VPCCidrBlock'
    code_commit_repo = 'AWS::CodeCommit::Repository'
    code_pipeline = 'AWS::CodePipeline::Pipeline'
    hosted_zone = 'AWS::Route53::HostedZone'
    acm_certificate = 'AWS::CertificateManager::Certificate'
    cw_log_group = 'AWS::Logs::LogGroup'
    helm_chart = 'Custom::AWSCDK-EKS-HelmChart'
    eks_query_object_value = 'Custom::AWSCDK-EKS-KubernetesObjectValue'
    route53_record_set = 'AWS::Route53::RecordSet'

    __test__ = False

    def test_s3_bucket_encryption(self):
        assert self.get_template_str().count(f'"{self.s3_bucket}"') == \
               self.get_template_str().count('"SSEAlgorithm":"aws:kms"') == \
               self.get_template_str().count('"ServerSideEncryptionConfiguration"') == \
               self.get_template_str().count('"BucketEncryption"')

    def test_s3_block_public_access(self):
        assert self.get_template_str().count(f'"{self.s3_bucket}"') == \
               self.get_template_str().count('"PublicAccessBlockConfiguration"') == \
               self.get_template_str().count('"BlockPublicAcls":true') == \
               self.get_template_str().count('"BlockPublicPolicy":true') == \
               self.get_template_str().count('"IgnorePublicAcls":true') == \
               self.get_template_str().count('"RestrictPublicBuckets":true')

    def test_kms_key_rotation_enabled(self):
        assert self.get_template_str().count(f'"{self.kms_key}"') == \
               self.get_template_str().count('"EnableKeyRotation":true')

    def test_s3_bucket_baseline(self):
        if self.get_template_str().count(f'"{self.s3_bucket}"'):
            expect(self.cfn_template).to(have_resource(self.s3_bucket, {
                "BucketEncryption": {
                    "ServerSideEncryptionConfiguration": [
                        {
                            "ServerSideEncryptionByDefault": {
                                "SSEAlgorithm": "aws:kms"
                            }
                        }
                    ]
                },
                "PublicAccessBlockConfiguration": {
                    "BlockPublicAcls": 'true',
                    "BlockPublicPolicy": 'true',
                    "IgnorePublicAcls": 'true',
                    "RestrictPublicBuckets": 'true'
                },
            }))

    def test_s3_bucket_enforce_encryption_policy_applied(self):

        assert self.get_template_str().count(f'"{self.s3_bucket_policy}"') == \
               self.get_template_str().count(f'"{self.s3_bucket}"')

        if self.get_template_str().count(f'"{self.s3_bucket_policy}"'):
            expect(self.cfn_template).to(have_resource(self.s3_bucket_policy, {
                "Bucket": {
                    "Ref": ANY_VALUE
                },
                "PolicyDocument": {
                    "Statement": [
                        {
                            "Action": "s3:*",
                            "Condition": {
                                "Bool": {
                                    "aws:SecureTransport": "false"
                                }
                            },
                            "Effect": "Deny",
                            "Principal": "*",
                            "Resource": [
                                {
                                    "Fn::GetAtt": [
                                        ANY_VALUE,
                                        "Arn"
                                    ]
                                },
                                {
                                    "Fn::Join": [
                                        "",
                                        [
                                            {
                                                "Fn::GetAtt": [
                                                    ANY_VALUE,
                                                    "Arn"
                                                ]
                                            },
                                            "/*"
                                        ]
                                    ]
                                }
                            ]
                        }
                    ],
                    "Version": "2012-10-17"
                }
            }))

    def test_no_iam_users_created(self):
        assert self.iam_user not in self.get_template_str()

    def test_no_iam_groups_created(self):
        assert self.iam_group not in self.get_template_str()

    def exists(self, value):
        exists = False
        exists = value.replace("\"", "\\\"") in self.get_template_str() or exists
        return exists

    def regex_search(self, value: typing.Pattern[typing.AnyStr]):
        exists = False
        exists = re.search(value, self.get_template_str()) or exists
        return exists

    def get_template_str(self):
        return json.dumps(self.cfn_template).replace(' ', '')

    @staticmethod
    def load_stack_template(stack_name: str):
        return read(f'{cdk_out_dir}/{stack_prefix}-{stack_name}.{suffix}')

