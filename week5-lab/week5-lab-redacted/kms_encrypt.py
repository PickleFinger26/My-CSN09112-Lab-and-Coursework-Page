"""AWS KMS encryption/decryption demo for Week 5 lab."""
import base64
import boto3
from botocore.exceptions import ClientError

AWS_REGION = "us-east-1"
KEY_ALIAS = "alias/MySymKey"
kms_client = boto3.client("kms", region_name=AWS_REGION)


def encrypt(secret, key_id):
    try:
        response = kms_client.encrypt(
            KeyId=key_id,
            Plaintext=secret.encode("utf-8"),
        )
    except ClientError:
        print("Problem with encryption.")
        raise
    return base64.b64encode(response["CiphertextBlob"])


def decrypt(ciphertext, key_id):
    try:
        response = kms_client.decrypt(
            KeyId=key_id,
            CiphertextBlob=base64.b64decode(ciphertext),
        )
    except ClientError:
        print("Problem with decryption.")
        raise
    return response["Plaintext"]


if __name__ == "__main__":
    print(f"Using KMS key: {KEY_ALIAS}")
    msg = "Hello"
    print(f"Plaintext: {msg}")
    cipher = encrypt(msg, KEY_ALIAS)
    print(f"Cipher (Base64): {cipher.decode('ascii')}")
    plaintext = decrypt(cipher, KEY_ALIAS)
    print(f"Plain: {plaintext.decode('utf-8')}")
    assert plaintext.decode("utf-8") == msg
    print("Encryption and decryption verified!")
