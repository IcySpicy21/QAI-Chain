def proof_of_work(block, difficulty):

    prefix = "0" * difficulty

    while not block.hash.startswith(prefix):

        block.nonce += 1
        block.hash = block.compute_hash()

    return block