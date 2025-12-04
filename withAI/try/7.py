import torch
import torch.nn as nn

torch.manual_seed(42)

class SHA(nn.Module):

    def __init__(self,dim_model,dim_QKV=8):
        super().__init__()

        self.fc_q = nn.Linear(dim_model,dim_QKV)
        self.fc_k = nn.Linear(dim_model,dim_QKV)
        self.fc_v = nn.Linear(dim_model,dim_QKV)
        self.dim_QKV = dim_QKV

    def forward(self,x):

        Q = self.fc_q(x)
        K = self.fc_k(x)
        V = self.fc_k(x)

        K_t = K.transpose(-2,-1)
        attn_scores = Q @ K_t

        scaled_scores = attn_scores / torch.sqrt(torch.tensor(self.dim_QKV))
        rates = torch.softmax(scaled_scores, dim=-1)

  
        