import torch
import torch.nn as nn

from quantum.kernels.quantum_kernel import quantum_kernel


class QuantumAttention(nn.Module):

    def __init__(self):
        super().__init__()

    def forward(self, x):
        """
        x: [batch, seq_len, dim]
        """

        batch_size, seq_len, dim = x.shape

        outputs = []

        for b in range(batch_size):

            seq = x[b]

            attention_matrix = torch.zeros(seq_len, seq_len)

            # compute quantum similarities
            for i in range(seq_len):
                for j in range(seq_len):

                    attention_matrix[i, j] = quantum_kernel(seq[i], seq[j])

            # normalize
            attention_weights = torch.softmax(attention_matrix, dim=-1)

            # weighted sum
            context = torch.matmul(attention_weights, seq)

            outputs.append(context)

        return torch.stack(outputs)