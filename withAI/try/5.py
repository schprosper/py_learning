import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader,Dataset
import os
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing  import StandardScaler
seed = 42
torch.manual_seed(seed)

# 数据获取
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir,'data.csv')

# 读取数据,数据处理
# 需要把数据读取到不同列,然后对颜色一行进行独热编码
# 之后,把需要的数据,放到dataset里面,之后放在dataLoader进行处理
# 然后得到的X,就可以当做数据导入进去了


# 先定义一下弹幕要的数据类型
class DanmuDataset(Dataset):
    def __init__(self,features,labels):
        super().__init__()
        self.features = torch.tensor(features,dtype=torch.float32)
        self.labels = torch.tensor(labels,dtype=torch.float32)


    def __len__(self):return len(self.features)
    def __getitem__(self, idx):
        return self.features[idx],self.labels[idx]
    

df = pd.read_csv(file_path)
X = df[["diameter", "speed", "color"]]    # 取出样本
y = df["power"].values # 取出代码,并且变成Numpy数组

x_encoded = pd.get_dummies(X,columns=["color"],)

# OK 数据,已经成为我们的编码了,也就是说,
# 我们现在对于Pandas方面的数据已经处理完成了
# 那么需要对Numpy进行处理了,对他,我们需要进行训练划分

X_train_val,X_test,y_train_val,y_test = train_test_split(x_encoded.values, y, test_size=0.2)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.125)
scaler = StandardScaler()
# 给训练集标准化
X_train_scaled = scaler.fit_transform(X_train)
# 训练划分完了需要进行放缩
X_val_scaled = scaler.transform(X_val) 
X_test_scaled = scaler.transform(X_test)

# 装载模型,首先转化成tensor
batch_size = 32
train_dataset = DanmuDataset(X_test_scaled,y_train)
val_dataset = DanmuDataset(X_val_scaled, y_val)
test_dataset = DanmuDataset(X_test_scaled, y_test)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)# 打乱保证训练有效性
# 测试集不打乱,因为模型不记录这些数据,模型好坏标准一致.
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)# 没必要打乱
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

class DanMuMLp(nn.Module):
    def __init__(self,input_dim,hidden_dim1=64,hidden_dim2=32,dropout =0.1):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim,hidden_dim1),
            nn.ReLU(),
            nn.Dropout(dropout),# 关闭了当前层的一些输出,也是一种正则化
            nn.Linear(hidden_dim1,hidden_dim2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim2,1)
        )
    def forward(self,x):
        return self.model(x)


input_dim = len(x_encoded.columns)

model = DanMuMLp(input_dim=input_dim, hidden_dim1=64, hidden_dim2=32)

creterion =  nn.MSELoss()
optimizer = optim.Adam(model.parameters(),lr=0.01,weight_decay=0.1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
# note the loss ,so we do pre raw
train_losses = [] # 这里真应该加入history
val_losses = []
# 训练开始,但是训练模式没有开启
for epcho in range(5):
    model.train()
    train_loss = 0.0
    for feature ,labels in train_loader:
        features, labels = features.to(device), labels.to(device)
        outputs = model(features)
        loss = creterion(outputs,labels)
        optimizer.zero_grad
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * features.size(0)
    train_loss_avg = train_loss / len(train_loader.dataset)
    train_losses.append(train_loss_=avg)

    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        # for fe lb = train_laoder:  
        # to divece
        # output 
        # loss 
        # sum loss = loss.item() * feature.size(0)
        # val_loss
        # all_val_loss 
    # no dont mind     

    # if (epoch)


    # finish print
    # 
    # 
#model.eval()
# test_preds = []
# test_ture  = []
#                      




