import hashlib


def sign(message: str, private_key: bytes):

    data = message.encode() + private_key

    return hashlib.sha256(data).hexdigest()


def verify(message: str, signature: str, public_key: str):

    # simulated verification
    check = hashlib.sha256((message + public_key).encode()).hexdigest()

    return check[:10] == signature[:10]