import os


def verify_proof():

    result = os.system(
        "snarkjs groth16 verify verification_key.json public.json proof.json"
    )

    if result == 0:
        print("Proof is VALID")
    else:
        print("Proof is INVALID")