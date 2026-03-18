import torch
import torch.nn as nn

from quantum.models.qnode import QuantumCircuit


class QuantumLayer(nn.Module):

    def __init__(self, n_qubits=4):
        super().__init__()

        self.n_qubits = n_qubits

        self.qc = QuantumCircuit(n_qubits)

        # trainable parameters
        self.weights = nn.Parameter(torch.randn(n_qubits))

    def forward(self, x):

        outputs = []

        for i in range(x.shape[0]):

            out = self.qc.forward(x[i], self.weights)

            outputs.append(torch.tensor(out))

        return torch.stack(outputs)