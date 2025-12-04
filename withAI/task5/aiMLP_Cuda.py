import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir,'data.csv')

# -------------------------- 1. 数据读取与预处理 --------------------------
class DanmuDataset(Dataset):
    """自定义数据集类，用于加载和处理弹幕数据"""
    def __init__(self, features, labels):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)  # 转为(batch_size, 1)格式

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

# 读取数据
df = pd.read_csv(file_path)
print("数据基本信息：")
print(df.info())
print("\n数据前5行：")
print(df.head())

# 分离特征和标签（英文列名匹配数据）
X = df[["diameter", "speed", "color"]]
y = df["power"].values

# 处理非数值特征（颜色独热编码）
X_encoded = pd.get_dummies(X, columns=["color"], prefix="color")
print("\n独热编码后的特征列：")
print(X_encoded.columns.tolist())

# 数据划分（训练集:验证集:测试集 = 7:1:2）
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X_encoded.values, y, test_size=0.2, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.125, random_state=42
)

# 特征标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

print(f"\n数据集大小：")
print(f"训练集：{X_train_scaled.shape}, 验证集：{X_val_scaled.shape}, 测试集：{X_test_scaled.shape}")

# 创建DataLoader
batch_size = 32
train_dataset = DanmuDataset(X_train_scaled, y_train)
val_dataset = DanmuDataset(X_val_scaled, y_val)
test_dataset = DanmuDataset(X_test_scaled, y_test)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# -------------------------- 2. MLP模型搭建（修复重复层问题） --------------------------
class DanmuMLP(nn.Module):
    """弹幕威力预测MLP模型（修正结构重复错误）"""
    def __init__(self, input_dim, hidden_dim1=64, hidden_dim2=32, dropout=0.1):
        super(DanmuMLP, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim1),  # 输入层→隐藏层1
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim1, hidden_dim2),  # 隐藏层1→隐藏层2
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim2, 1)  # 隐藏层2→输出层（仅1层输出）
        )

    def forward(self, x):
        return self.model(x)

# 初始化模型
input_dim = X_encoded.shape[1]
model = DanmuMLP(input_dim=input_dim, hidden_dim1=64, hidden_dim2=32)
print("\n模型结构：")
print(model)

# -------------------------- 3. 训练配置 --------------------------
epochs = 50
learning_rate = 1e-3
weight_decay = 1e-4

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, factor=0.5)

# -------------------------- 4. 模型训练与验证（强制使用GPU） --------------------------
# 强制使用GPU，若没有GPU会报错（符合用户"使用GPU"的要求）
device = torch.device("cuda:0")  # 指定使用第1块GPU
model.to(device)
print(f"\n使用设备：{device}")
print(f"GPU是否可用：{torch.cuda.is_available()}")
print(f"当前使用的GPU：{torch.cuda.get_device_name(device)}")

train_losses = []
val_losses = []

for epoch in range(epochs):
    # 训练阶段
    model.train()
    train_loss = 0.0
    for features, labels in train_loader:
        features, labels = features.to(device), labels.to(device)  # 数据移到GPU
        
        outputs = model(features)
        loss = criterion(outputs, labels)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        train_loss += loss.item() * features.size(0)
    
    train_loss_avg = train_loss / len(train_loader.dataset)
    train_losses.append(train_loss_avg)

    # 验证阶段
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for features, labels in val_loader:
            features, labels = features.to(device), labels.to(device)  # 数据移到GPU
            outputs = model(features)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * features.size(0)
    
    val_loss_avg = val_loss / len(val_loader.dataset)
    val_losses.append(val_loss_avg)

    scheduler.step(val_loss_avg)

    if (epoch + 1) % 5 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {train_loss_avg:.4f}, Val Loss: {val_loss_avg:.4f}")

print("\n训练完成！")

# -------------------------- 5. 模型评估（测试集） --------------------------
model.eval()
test_preds = []
test_trues = []

with torch.no_grad():
    for features, labels in test_loader:
        features, labels = features.to(device), labels.to(device)  # 数据移到GPU
        outputs = model(features)
        test_preds.extend(outputs.cpu().numpy())  # 转回CPU用于计算指标
        test_trues.extend(labels.cpu().numpy())

test_preds = np.array(test_preds)
test_trues = np.array(test_trues)

mse = mean_squared_error(test_trues, test_preds)
rmse = np.sqrt(mse)
mae = mean_absolute_error(test_trues, test_preds)

print("\n测试集评估结果：")
print(f"均方误差 (MSE): {mse:.4f}")
print(f"均方根误差 (RMSE): {rmse:.4f}")
print(f"平均绝对误差 (MAE): {mae:.4f}")

# -------------------------- 6. 结果可视化 --------------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(12, 4))

# 损失曲线
plt.subplot(1, 2, 1)
plt.plot(range(1, epochs+1), train_losses, label='训练损失')
plt.plot(range(1, epochs+1), val_losses, label='验证损失')
plt.xlabel('训练轮数')
plt.ylabel('MSE损失')
plt.title('训练与验证损失曲线')
plt.legend()
plt.grid(True, alpha=0.3)

# 预测散点图
plt.subplot(1, 2, 2)
plt.scatter(test_trues, test_preds, alpha=0.6)
plt.plot([test_trues.min(), test_trues.max()], [test_trues.min(), test_trues.max()], 'r--', label='理想预测线')
plt.xlabel('真实威力值')
plt.ylabel('预测值')
plt.title(f'预测值 vs 真实值 (RMSE={rmse:.4f})')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# -------------------------- 7. 模型保存 --------------------------
model_path = os.path.join(script_dir, 'danmu_mlp_model.pth')
torch.save(model.state_dict(), model_path)
print(f"\n模型已保存为: {model_path}")