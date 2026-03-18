import torch
import torch.nn as nn
import warnings

warnings.filterwarnings("ignore", message="Converting a tensor with requires_grad=True to a scalar may lead to unexpected behavior.*")

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
            import numpy as np
            # Convert to numpy, then to float32 for PyTorch
            if isinstance(out, torch.Tensor):
                out = out.detach().cpu().numpy()
            if isinstance(out, (np.generic, np.ndarray)) and out.shape == ():
                out = out.item()
            # Always cast to float32 for PyTorch compatibility
            out = np.array(out, dtype=np.float32)
            outputs.append(torch.as_tensor(out, dtype=torch.float32))

        return torch.stack(outputs)