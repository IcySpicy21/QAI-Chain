import torch
from pathlib import Path

from ai.rl.environment import BlockchainEnv
from ai.models.metrics_encoder import MetricsEncoder
from ai.models.policy_network import PolicyNetwork
from ai.models.value_network import ValueNetwork
from ai.rl.ppo_agent import PPOAgent


def train(blockchain, episodes=50):

    env = BlockchainEnv(blockchain)

    encoder = MetricsEncoder()
    policy = PolicyNetwork()
    value = ValueNetwork()

    agent = PPOAgent(policy, value)
    episode_rewards = []
    ma_window = 10
    best_ma_reward = float("-inf")

    entropy_start = 0.01
    entropy_end = 0.002

    checkpoint_dir = Path(__file__).resolve().parents[2] / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    best_checkpoint_path = checkpoint_dir / "best_rl_checkpoint.pt"

    for ep in range(episodes):
        # Linearly decay entropy to reduce late-training volatility.
        progress = ep / max(1, episodes - 1)
        agent.entropy_coef = entropy_start + (entropy_end - entropy_start) * progress

        state = env.reset()

        states = []
        actions = []
        log_probs = []
        rewards = []

        for step in range(30):

            encoded = encoder(torch.tensor(state).float().unsqueeze(0))

            action, log_prob = agent.select_action(encoded.detach().numpy()[0])

            next_state, reward, done = env.step(action)

            states.append(encoded.detach().numpy()[0])
            actions.append(action)
            log_probs.append(log_prob)
            rewards.append(reward)

            state = next_state

        returns = agent.compute_returns(rewards)

        agent.ppo_update(states, actions, log_probs, returns)

        total_reward = float(sum(rewards))
        episode_rewards.append(total_reward)
        recent_rewards = episode_rewards[-ma_window:]
        moving_avg_reward = sum(recent_rewards) / len(recent_rewards)

        if moving_avg_reward > best_ma_reward:
            best_ma_reward = moving_avg_reward
            torch.save(
                {
                    "episode": ep,
                    "ma_reward": moving_avg_reward,
                    "policy_state_dict": policy.state_dict(),
                    "value_state_dict": value.state_dict(),
                    "optimizer_state_dict": agent.optimizer.state_dict(),
                },
                best_checkpoint_path,
            )

        print(
            f"Episode {ep} | Reward: {total_reward:.2f} | "
            f"MA{ma_window}: {moving_avg_reward:.2f} | "
            f"Difficulty: {blockchain.difficulty} | "
            f"Entropy: {agent.entropy_coef:.4f}"
        )

    print(f"Best MA{ma_window}: {best_ma_reward:.2f} | Checkpoint: {best_checkpoint_path}")