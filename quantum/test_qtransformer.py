import torch
from quantum.transformer.q_transformer import QTransformer


model = QTransformer()

# batch=2, seq_len=4, features=5
x = torch.randn(2, 4, 5)

out = model(x)

print("Output:", out)