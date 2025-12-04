import torch
import torch.nn as nn

torch.manual_seed()

class Single_Head_Attention(nn.Module):

    def __init__(self,dim_model,dim_QKV=8):
        super().__init__()


        # QKV输出唯独必须一样
        self.fc_q = nn.Linear(dim_model,dim_QKV)
        self.fc_k = nn.Linear(dim_model,dim_QKV)
        self.fc_v = nn.Linear(dim_model,dim_QKV)
        # 为后续注意力分数放缩提供参数
        self.dim_QKV = dim_QKV


    def forward(self,x):
        """
        x 输入张量，形状[batch_size, seq_len, d_model]二维
        输出:[batch_size, seq_len, d_model] 注意力加权输出
        """
        # 原始特征变为三个空间
        Q = self.fc_q(x)
        K = self.fc_k(x)
        V = self.fc_k(x)

        #用负数索引定位「最后几个维度」，不管张量总共有多少维，只交换最后两个维度
        K_t = K.transpose(-2,-1)
        attn_scores = Q @ K_t

        # 缩放避免梯度消失,除以根号下 QKV的唯独
        scaled_scores = attn_scores / torch.sqrt(torch.tensor(self.dim_QKV,dtype=torch.float32))
        # 计算概率
        weights = torch.softmax(scaled_scores, dim=-1)

        self._judge(weights)

        output = weights @ V

        return output,weights
    

    def _judge(self,weight):

        line_sums= torch.sum(weight,dim=-1)
        
        print(f"归一缩放情况:{line_sums.min()},{line_sums.max()}")

        compare_line_sums = torch.ones_like(line_sums)

        # 这里必须必须考虑浮点精度问题
        if torch.all(weight >= -1e-6) & torch.all(torch.isclose(line_sums,compare_line_sums,atol = 1e-6)):
            print("概率计算合法")
            
        else :print ("概率计算错误")



if __name__ == "__main__":

    batch_size = 2
    seq_len = 4
    dim_model = 64

    x = torch.randn(batch_size,seq_len,dim_model)

    attn_block = Single_Head_Attention(dim_model=dim_model,dim_QKV=8)

    output , weights = attn_block(x)

    print("加权后的V:")
    print(output[0, :5, :9].detach().numpy().round(3))


    










        








    