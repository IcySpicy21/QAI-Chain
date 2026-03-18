import torch
import torch.nn as nn
import torch.optim as optim


class PPOAgent:

    def __init__(self, policy, value, lr=3e-4):

        self.policy = policy
        self.value = value

        self.optimizer = optim.Adam(
            list(policy.parameters()) + list(value.parameters()),
            lr=lr
        )

        self.gamma = 0.99
        self.eps_clip = 0.2

    def select_action(self, state):

        state = torch.tensor(state).float().unsqueeze(0)

        mean, std = self.policy(state)

        dist = torch.distributions.Normal(mean, std)

        action = dist.sample()

        log_prob = dist.log_prob(action)

        return action.item(), log_prob

    def compute_returns(self, rewards):

        returns = []

        G = 0

        for r in reversed(rewards):
            G = r + self.gamma * G
            returns.insert(0, G)

        return torch.tensor(returns)

    def ppo_update(self, states, actions, old_log_probs, returns):

        states = torch.tensor(states).float()
        actions = torch.tensor(actions).float()
        old_log_probs = torch.stack(old_log_probs).detach()
        returns = returns.detach()

        mean, std = self.policy(states)

        dist = torch.distributions.Normal(mean, std)

        new_log_probs = dist.log_prob(actions)

        ratio = torch.exp(new_log_probs - old_log_probs)

        clipped_ratio = torch.clamp(ratio, 1 - self.eps_clip, 1 + self.eps_clip)

        policy_loss = -torch.min(ratio * returns, clipped_ratio * returns).mean()

        value_pred = self.value(states).squeeze()

        value_loss = (returns - value_pred).pow(2).mean()

        loss = policy_loss + 0.5 * value_loss

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
            