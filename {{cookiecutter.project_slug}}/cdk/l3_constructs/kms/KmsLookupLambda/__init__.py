import os
import time
import uuid
import boto3
import logging as log


def get_boto3_client(service_name: str, credentials=None, region: str=None):
    assert service_name
    if credentials:
        client = boto3.client(service_name,
                              aws_access_key_id=credentials['AccessKeyId'],
                              aws_secret_access_key=credentials['SecretAccessKey'],
                              aws_session_token=credentials['SessionToken'],
                              region_name=region or None)
    else:
        client = boto3.client(service_name, region_name=region or None)

    return client


def assume_role(account_id, role_name, credentials=None):
    sts_client = get_boto3_client(service_name='sts', credentials=credentials)
    role_arn = 'arn:aws:iam::' + account_id + ':role/' + role_name
    assuming_role = True
    assumed_role_object = {}
    while assuming_role is True:
        try:
            assuming_role = False
            assumed_role_object = sts_client.assume_role(
                RoleArn=role_arn,
                RoleSessionName="GetKmsKeyId"
            )
        except Exception as e:
            assuming_role = True
            print(e)
            print("Retrying...")
            time.sleep(10)
    print('AssumedRole: RoleArn = {} , RoleSessionName'.format(role_arn))
    # From the response that contains the assumed role, get the temporary
    # credentials that can be used to make subsequent API calls
    return assumed_role_object['Credentials']


def lambda_handler(event, context):
    print(event)
    physical_id = f'GetKmsKeyId-{uuid.uuid4()}'
    log.getLogger().setLevel(log.WARN)

    assert 'AwsAccountId' in os.environ
    assert 'AwsRegion' in os.environ
    assert 'RoleName' in os.environ
    assert 'KmsAlias' in event["ResourceProperties"]

    cfn_response = {}
    try:
        account_id = os.environ['AwsAccountId']
        aws_region = os.environ['AwsRegion']
        role_name = os.environ['RoleName']

        props = event["ResourceProperties"]

        kms_alias = props['KmsAlias']

        credentials = assume_role(account_id=account_id, role_name=role_name)

        kms = get_boto3_client(service_name='kms', credentials=credentials, region=aws_region)

        response = kms.describe_key(
            KeyId=f'alias/{kms_alias}'
        )

        arn = response['KeyMetadata']['Arn']

        if arn:
            cfn_response = {
                "Data": {
                    "Arn": arn
                }
            }

        print(f'KMS Key Arn: {arn}, cfn_response: {cfn_response}')
    except Exception as e:
        print(f"Exception {e}")
        log.exception(e)

    return cfn_response
