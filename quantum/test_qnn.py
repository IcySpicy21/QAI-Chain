import torch
from quantum.models.qnn import QNN


model = QNN()

x = torch.randn(2, 5)

out = model(x)

print("Quantum Output:", out)