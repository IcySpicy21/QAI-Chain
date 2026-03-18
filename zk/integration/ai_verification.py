from zk.prover.generate_proof import generate_proof
from zk.verifier.verify_proof import verify_proof


def verify_ai_inference():

    print("Running AI inference with proof...")

    generate_proof()

    verify_proof()