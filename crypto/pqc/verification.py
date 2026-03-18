from crypto.pqc.signature import verify


def verify_transaction(tx, public_key):

    message = str(tx.to_dict())

    return verify(message, tx.signature, public_key)