import json
import os
import boto3
import botocore
from botocore.exceptions import ClientError


class AmazonSecretsManager:
    secret_name = None
    region = None

    def __init__(self, secret_name, region):
        self.client = None
        self.secret_name = secret_name
        self.region = region

    def get_secret(self, queryKey: str) -> str:
        """ Gets a secret from AWS.

        :param queryKey:
        :type queryKey:
        :return:
        :rtype:
        """
        try:
            aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
            aws_session_token = os.environ.get('AWS_SESSION_TOKEN')
            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_key_name = os.environ.get('AWS_SECRET_KEY_NAME')

            self.client = boto3.client('secretsmanager',
                                       aws_secret_access_key=aws_secret_access_key,
                                       aws_session_token=aws_session_token,
                                       region_name=self.region,
                                       aws_access_key_id=aws_access_key_id
                                       )

            response = json.loads(self.client.get_secret_value(SecretId=aws_secret_key_name)["SecretString"])
            return response[queryKey]
        except botocore.exceptions.ClientError as e:
            error_message = f"Error getting {queryKey} secret from Secrets Manager: {e}"
            raise Exception(error_message)
