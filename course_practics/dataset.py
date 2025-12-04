
import numpy as np
import torch

np_coffee = np.array([[200,17],[185,19],[210,15],[195,18],[175,21]])
torch_coffee = torch.from_numpy(np_coffee).to(dtype=torch.float32)
'''
print(f'{np_coffee.shape},{np_coffee.dtype},{torch_coffee.shape},{torch_coffee.dtype}')
sample_coffee = np_coffee[2,0]
sample_torch_coffee = torch_coffee[2,0]
value_sample_coffee = torch_coffee[2,0].item()
print(f"{sample_coffee},{value_sample_coffee},{sample_torch_coffee}")
print("sample_torch_coffee 类型：", type(sample_torch_coffee))
'''
# 练习题 2：PyTorch 张量运算与 NumPy 互转模拟全连接神经元层的（神经网络前向传播模拟）
torch.manual_seed(42)
w_1 = torch.randn((2,3),dtype=torch.float32)
b_1 = torch.full((1,3),0.1,dtype=torch.float32)

h1 = torch.relu((torch_coffee @ w_1) + b_1)
'''
5x2 @ 2x3
为什么需要这么乘?按照我们的运算顺序,这里指的是:
对于本层的一个神经元,我们需要接受上层两个神经元的影响.
本层的神经元一个一个算,本层神经元有几个就算几个.

我们这里五个样本全输入去,也就是我们最后会得到五个概率值,和_一次进行一个样本的预测,并不矛盾


'''
np_h1 = h1.numpy()

np_mui = h1.detach().numpy() - np_h1
np_max = np.max(np.abs(np_mui))

print(f"{np_max}")

w_2 = torch.randn((3,1),dtype=torch.float32)
b_2 = torch.full((1,1),0.05,dtype=torch.float32)

y_pred = torch.sigmoid(torch.matmul(h1, w_2) + b_2)
np_y = y_pred.numpy()
print(f"{np_y.shape},{y_pred}")


