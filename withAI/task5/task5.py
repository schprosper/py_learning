import os
import matplotlib.pyplot as plt
import random 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error , mean_absolute_error
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset,DataLoader #数据集和数据搬运并行运算


seed = 114  # 任意固定整数
random.seed(seed)  # Python 原生随机数种子
np.random.seed(seed)  # NumPy 随机数种子
torch.manual_seed(seed)  # PyTorch CPU 随机数种子

# 参数调节位置
dropout1 = 0.1
weight_decay = 0.01
epochs = 100
learning_rate = 0.1

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir,'data.csv')

# 读取并预处理数据
class DanmuDataset(Dataset):
    def __init__(self,features,labels):#本身,参数,答案
        super().__init__()
        self.features = torch.tensor(features,dtype=torch.float32)
        self.labels = torch.tensor(labels,dtype=torch.float32)

    def __len__(self) : return len(self.features)
    def __getitem__(self, idx):
        return self.features[idx],self.labels[idx]
    
df = pd.read_csv(file_path)
X = df[["diameter", "speed", "color"]]    # 取出样本

y = df["power"].values # 取出代码,并且变成Numpy数组

X_encoded = pd.get_dummies(X, columns=["color"], prefix="color")# 其余的不变,对color进行转化,返回的仍然是完整的训练集
# 划分:训练集+评估集+测试集

X_train_val,X_test,y_train_val,y_test = train_test_split(X_encoded.values, y, test_size=0.2)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.125)

# 标准化加快梯度

scaler = StandardScaler()

# 给训练集标准化

X_train_scaled = scaler.fit_transform(X_train)

# 先学习标准差和平均数,顺便标准化训练集
# 必须用训练集来标准化----保证,训练集的尺度特征可以泛化到所有集
# 保证模型对没见过的数据的彻彻底底的无知
X_val_scaled = scaler.transform(X_val) 
X_test_scaled = scaler.transform(X_test)

# 创建可以喂给torch的数据集
batch_size = 32
train_dataset = DanmuDataset(X_test_scaled,y_train)
val_dataset = DanmuDataset(X_val_scaled, y_val)
test_dataset = DanmuDataset(X_test_scaled, y_test)

# 创建数据流

# 这里打乱,数据库里面,红色弹幕出现的有规律
# 这个数据类型已经划开不同的batch了,把他当做数据集直接传入
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)# 打乱保证训练有效性
# 测试集不打乱,因为模型不记录这些数据,模型好坏标准一致.
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)# 没必要打乱
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)


# 模型搭建

class DanmuMLP(nn.Module):
    def __init__(self ,input_dim,hidden_dim1=64,hidden_dim2=32,dropout=dropout1):
        super().__init__()# 必须保证索引到前面一层
        self.model = nn.Sequential(
            nn.Linear(input_dim,hidden_dim1),
            nn.ReLU(),
            nn.Dropout(dropout),# 关闭了当前层的一些输出,也是一种正则化
            nn.Linear(hidden_dim1,hidden_dim2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim2,1)
        )
    # 调用接口,说是为了方便之后进行扩展操作
    def forward(self, x):
        return self.model(x)
    
input_dim = X_encoded.shape[1] # 这里是通用方法,获取维度,而不是说我知道有多少维度
# 要训练的模型
model = DanmuMLP(input_dim=input_dim, hidden_dim1=64, hidden_dim2=32)



# 用平均方差来看拟合程度
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(),lr=learning_rate,weight_decay=weight_decay)
# 这里已经完成了参数绑定
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, factor=0.5)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


train_losses = []
val_losses = []

# 每进行训练一次都记录一次数据
for epoch in range(epochs):
    # 开启训练模式
    model.train()
    train_loss = 0.0
    for features, labels in train_loader:
        features, labels = features.to(device), labels.to(device)
        outputs = model(features)# 输出最终弹幕的威力
        loss = criterion(outputs, labels)
        optimizer.zero_grad() # 清空原有梯度
        loss.backward() # 计算现在梯度
        optimizer.step() # 把梯度加上到参数里面
        train_loss += loss.item() * features.size(0)
    train_loss_avg = train_loss / len(train_loader.dataset)
    train_losses.append(train_loss_avg)


    # 验证集评估,(给出训练的流程)
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for features, labels in val_loader:
            features, labels = features.to(device), labels.to(device)
            outputs = model(features)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * features.size(0)
    val_loss_avg = val_loss / len(val_loader.dataset)
    val_losses.append(val_loss_avg)

    scheduler.step(val_loss_avg)
    if (epoch + 1) % 5 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss_avg:.4f}, Val Loss: {val_loss_avg:.4f}")

print("\n训练完成！")

# 测试集评估
model.eval()
test_preds = []
test_trues = []
with torch.no_grad():
    for features, labels in test_loader:
        features, labels = features.to(device), labels.to(device)
        outputs = model(features)
        test_preds.extend(outputs.cpu().numpy())
        '''
        对输出进行格式转换,把张量移动到CPU,然后再转化成Numpy数组,更方便之后的计算
        extend() 会把当前 batch 的预测结果（NumPy 数组）加到列表里，
        最终 test_preds 会包含测试集所有样本的预测结果。
        '''
        test_trues.extend(labels.cpu().numpy())

test_preds = np.array(test_preds)# 把列表转化为np数组,为了喂给之后的评估函数
test_trues = np.array(test_trues)
mse = mean_squared_error(test_trues, test_preds)#sklearn.metrics需要 NumPy 数组 作为输入

print("\n测试集评估：")
print(f"MSE: {mse:.4f} ")
