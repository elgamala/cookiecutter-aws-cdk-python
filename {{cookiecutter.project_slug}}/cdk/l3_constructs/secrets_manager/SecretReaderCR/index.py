import boto3
import uuid
import json
import logging as log
sm = boto3.client('secretsmanager')


def handler(event, context):
    log.getLogger().setLevel(log.INFO)

    physical_id = f'SecretReader-{uuid.uuid4()}'

    try:
        log.info('Input event: %s', event)

        if event['RequestType'] != 'Create':
            return {'Data': {}}

        # Check if this is a Create and we're failing Creates
        if event['RequestType'] == 'Create' and event['ResourceProperties'].get('FailCreate', False):
            raise RuntimeError('Create failure requested')

        # Do the thing
        data = event['ResourceProperties']
        if data:

            response = sm.get_secret_value(
                SecretId=data['SecretArn']
            )

            if 'AttributeName' in data:
                attributes = {
                    'Data': {
                        'SecretValue': json.loads(response['SecretString'])[data['AttributeName']]
                    }
                }
            else:
                attributes = {
                    'Data': {
                        'SecretValue': response['SecretString']
                    }
                }
        else:
            attributes = {'Data': {}}

        return attributes

    except Exception as e:
        log.exception(e)
        return {'Data': {}}


