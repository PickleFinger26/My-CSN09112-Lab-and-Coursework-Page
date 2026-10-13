# Week 5 Lab — AWS Key Management Service (KMS)

## Objective
Create a customer-managed symmetric AWS KMS key and use it to encrypt and decrypt data with both the AWS CLI and Python Boto3.

## Environment
- AWS Academy Learner Lab (temporary lab credentials)
- Region: `us-east-1`
- KMS key alias: `alias/MySymKey`
- AWS CLI and Python with Boto3


## Tasks completed
1. Created and enabled a symmetric customer-managed key named `MySymKey`.
2. Configured valid temporary AWS CLI credentials for the Learner Lab.
3. Encrypted a text file with `aws kms encrypt`.
4. Decoded the Base64 ciphertext into a binary file.
5. Decrypted the binary ciphertext using `aws kms decrypt` and restored the plaintext.
6. Implemented a Python Boto3 example with `kms.encrypt()` and `kms.decrypt()`.
7. Confirmed the Python message `Hello` was recovered after decryption.

## CLI demonstration
Create a harmless local sample file:

```bash
printf 'This is my super secret file.\n' > 1.txt
```

Check authentication (after securely setting up your Learner Lab credentials):

```bash
aws sts get-caller-identity
```

Encrypt and decode ciphertext:

```bash
aws kms encrypt --region us-east-1 --key-id alias/MySymKey \
  --plaintext fileb://1.txt --query CiphertextBlob --output text > 1.out
base64 --decode 1.out > 1.enc
```

Decrypt and verify the original contents:

```bash
aws kms decrypt --region us-east-1 --key-id alias/MySymKey \
  --ciphertext-blob fileb://1.enc --query Plaintext --output text > 2.out
base64 --decode 2.out > decrypted.txt
diff 1.txt decrypted.txt
```

A successful `diff` produces no output.

## Python demonstration
Install dependencies in an environment with a supported Python version:

```bash
python3 -m pip install -r requirements.txt
python3 kms_encrypt.py
```

Expected behavior:

```text
Using KMS key: alias/MySymKey
Plaintext: Hello
Cipher (Base64): <Base64 ciphertext varies>
Plain: Hello
Encryption and decryption verified!
```

## Issues encountered and resolution
- `InvalidClientTokenId` / `UnrecognizedClientException`: stale AWS CLI credentials. Obtained current temporary credentials from Learner Lab **AWS Details → AWS CLI** and used a separate credentials file when the lab-managed one was not writable.
- `AccessDenied` for unrelated console operations: Learner Lab permission restrictions; avoided unauthorized operations.
- Python 3.7 / Boto3 deprecation warning: code executed, but future development should use a supported Python version.

## What I learned
AWS KMS protects encryption keys and provides API operations for encrypting and decrypting data. CLI ciphertext can be represented as Base64 text for transport, while the KMS decrypt API expects binary ciphertext. Temporary lab credentials must be valid before calling KMS.
