import numpy as np


class BlockchainEnv:

    def __init__(self, blockchain):

        self.blockchain = blockchain

        self.state_dim = 5
        self.action_dim = 3  # actions map to {-1, 0, +1} difficulty delta
        self.min_difficulty = 1
        self.max_difficulty = 8
        self.target_difficulty = 3

    def reset(self):

        return self.get_state()

    def get_state(self):

        chain = self.blockchain.chain

        num_blocks = len(chain)

        if num_blocks < 2:
            return np.zeros(self.state_dim)

        block_sizes = [len(b.transactions) for b in chain]

        avg_block_size = np.mean(block_sizes)
        tx_count = sum(block_sizes)

        avg_tx_per_block = tx_count / num_blocks

        fork_rate = 0.0  # placeholder
        latency = 1.0    # placeholder

        return np.array([
            num_blocks,
            avg_block_size,
            avg_tx_per_block,
            fork_rate,
            latency
        ], dtype=np.float32)

    def step(self, action):
        delta = float(np.clip(action, -1.0, 1.0))

        next_difficulty = np.clip(
            float(self.blockchain.difficulty) + delta,
            self.min_difficulty,
            self.max_difficulty,
        )
        self.blockchain.difficulty = int(round(next_difficulty))

        reward = self.compute_reward()

        next_state = self.get_state()

        done = False

        return next_state, reward, done

    def compute_reward(self):

        chain = self.blockchain.chain

        num_blocks = len(chain)

        if num_blocks == 0:
            return 0.0

        block_sizes = [len(b.transactions) for b in chain]

        throughput = sum(block_sizes) / num_blocks

        latency = 1.0 / max(1, self.blockchain.difficulty)
        decentralization = 1.0

        # Keep a smooth optimum around target difficulty.
        target_penalty = 0.2 * abs(self.blockchain.difficulty - self.target_difficulty)

        reward = (
            1.0 * throughput
            + 0.8 * latency
            + 0.5 * decentralization
            - target_penalty
        )

        return reward