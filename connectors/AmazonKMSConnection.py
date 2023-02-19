from libraries.FlaskRESTServiceLayer.connections import AbstractKMSConnection as kms
import boto3

class AmazonKMSConnection(kms.AbstractKMSConnection):

    def __init__(self):
        self.client = boto3.client('kms')

    def encrypt(self, plaintext):
        pass

    def decrypt(self, ciphertext):
        pass