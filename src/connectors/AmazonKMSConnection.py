import os
import boto3


class AmazonKMSConnection:
    client = None

    def __init__(self):
        aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_session_token = os.environ.get('AWS_SESSION_TOKEN')
        self.client = boto3.client('kms',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key,
                                   aws_session_token=aws_session_token)

    def generateDataKeys(self, keyID):
        """ Generates the data keys used for encryption and decryption.

        The ciphertext data key is used to securely transmit or store the data key, while keeping the key secret.
        When you generate a data key using AWS KMS, the generate_data_key method returns both the plaintext data key and
        an encrypted copy of the data key.

        The plaintext data key is used to encrypt and decrypt your data, while the ciphertext data key is used to
        securely transmit or store the data key. You should never transmit the plaintext data key over an unsecured
        network or store it in plain text on disk or in memory. Instead, you should use the encrypted copy of the data
        key to safely transmit the data key to other services or to store it securely.

        The ciphertext data key is encrypted using the KMS master key that was used to encrypt the data key. This means
        that only AWS KMS can decrypt the ciphertext data key and retrieve the plaintext data key. When you need to
        decrypt your data, you'll need to use the KMS master key to decrypt the ciphertext data key and retrieve the
        plaintext data key.

        By separating the plaintext data key from the ciphertext data key, AWS KMS provides an additional layer of
        security and helps you protect your data key in transit and at rest. This is important when dealing with
        sensitive data that needs to be protected from unauthorized access or tampering.


        :return:
        :rtype:
        """
        response = self.client.generate_data_key(KeyId=keyID)

        # Return the plaintext data key and the ciphertext data key
        return response['Plaintext'], response['CiphertextBlob']

    def decryptCiphertextDataKey(self, ciphertext_data_key):
        """ Decrypts the specified ciphertext data key using the KMS Key.

        The ciphertext key is an encrypted version of the plaintext key, it is encrypted using a key which is securely
        stored in the AWS KMS. When we provide the ciphertext version of the key to AWS it will return with the
        plaintext version.

        The ciphertext data key is designed to be transported and stored, unliked the plaintext key.

        :return:
        :rtype:
        """
        # Decrypt the specified ciphertext using the KMS key
        response = self.client.decrypt(CiphertextBlob=ciphertext_data_key)

        # Return the plaintext data key
        return response['Plaintext']
