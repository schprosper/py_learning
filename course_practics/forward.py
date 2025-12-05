import torch
import numpy as np

x = np.array([200,11])
w1_1 = np.array([0.1,0.2])
b1_1 = np.array([1])
'''一维数组用@会执行向量点积（是可以运行的）'''
z1_1 = np.array((w1_1 @ x) + b1_1)
# 其余前向同理

x = np.array([200,11])
w1_2 = np.array([0.1,0.2])
b1_2 = np.array([1])
z1_2 = np.array((w1_2 @ x) + b1_2)

x = np.array([200,11])
w1_3 = np.array([0.1,0.2])
b1_3 = np.array([1])
z1_3 = np.array((w1_3 @ x) + b1_3) 

# 这里不需要进行array的包裹---


#  进入下一层了,吗?
'''
作为神经网络,千万别忘了要进行激活函数----
这样就不会 ([z1.z2,z3])// 维度本身不会升高! 那是点乘得到数值啊
但是激活函数还是要有的....
'''
# 先转化成tensor才能用激活函数
z1 = np.array([z1_1,z1_2,z1_3])
z1_tensor = torch.from_numpy(z1).to(dtype=torch.float32)
a1_tensor = torch.sigmoid(z1_tensor)
a1 = a1_tensor.numpy()
# 首先要对输出进行整合


w2_1 = np.array([0.1,0.2,0.3])
b2_1 = np.array([1])
Number = (w2_1 @ a1) + b2_1
a2_1 = np.array(Number)

print(f"{a2_1}")