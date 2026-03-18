import torch
import torch.nn as nn


class PolicyNetwork(nn.Module):

    def __init__(self, input_dim=128, action_dim=3):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def forward(self, x):
        return self.net(x)