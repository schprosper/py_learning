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

# 保留你的路径读取逻辑
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir,'data.csv')

# -------------------------- 1. 数据读取与预处理（完全保留你的逻辑） --------------------------
class DanmuDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)
    def __len__(self): return len(self.features)
    def __getitem__(self, idx): return self.features[idx], self.labels[idx]

# 读取数据（去掉冗余打印）
df = pd.read_csv(file_path)
X = df[["diameter", "speed", "color"]]
y = df["power"].values

# 独热编码+数据划分+标准化（完全保留你的步骤）
X_encoded = pd.get_dummies(X, columns=["color"], prefix="color")
X_train_val, X_test, y_train_val, y_test = train_test_split(X_encoded.values, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.125, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)
# 
# 创建DataLoader（完全保留）
batch_size = 32
train_dataset = DanmuDataset(X_train_scaled, y_train)
val_dataset = DanmuDataset(X_val_scaled, y_val)
test_dataset = DanmuDataset(X_test_scaled, y_test)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# -------------------------- 2. 模型搭建（完全保留你的结构） --------------------------
class DanmuMLP(nn.Module):
    def __init__(self, input_dim, hidden_dim1=64, hidden_dim2=32, dropout=0.1):
        super(DanmuMLP, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim1),
            nn.ReLU(),
            nn.Dropout(dropout),# 关闭了当前层的一些输出
            nn.Linear(hidden_dim1, hidden_dim2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim2, 1)
        )
    def forward(self, x): return self.model(x)

input_dim = X_encoded.shape[1]
model = DanmuMLP(input_dim=input_dim, hidden_dim1=64, hidden_dim2=32)

# -------------------------- 3. 训练配置（完全保留你的参数） --------------------------
epochs = 50
learning_rate = 1e-3
weight_decay = 1e-4

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, factor=0.5)

# -------------------------- 4. 模型训练与验证（保留强制GPU逻辑） --------------------------
device = torch.device("cuda:0")
model.to(device)
print(f"使用设备：{device} | GPU可用：{torch.cuda.is_available()}")

train_losses = []
val_losses = []

for epoch in range(epochs):
    # 训练
    model.train()
    train_loss = 0.0
    for features, labels in train_loader:
        features, labels = features.to(device), labels.to(device)
        outputs = model(features)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * features.size(0)
    train_loss_avg = train_loss / len(train_loader.dataset)
    train_losses.append(train_loss_avg)

    # 验证
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

# -------------------------- 5. 模型评估（保留完整指标） --------------------------
model.eval()
test_preds = []
test_trues = []
with torch.no_grad():
    for features, labels in test_loader:
        features, labels = features.to(device), labels.to(device)
        outputs = model(features)
        test_preds.extend(outputs.cpu().numpy())
        test_trues.extend(labels.cpu().numpy())

test_preds = np.array(test_preds)
test_trues = np.array(test_trues)
mse = mean_squared_error(test_trues, test_preds)
rmse = np.sqrt(mse)
mae = mean_absolute_error(test_trues, test_preds)

print("\n测试集评估：")
print(f"MSE: {mse:.4f} | RMSE: {rmse:.4f} | MAE: {mae:.4f}")












# -------------------------- 6. 结果可视化（保留你的图表） --------------------------
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(range(1, epochs+1), train_losses, label='训练损失')
plt.plot(range(1, epochs+1), val_losses, label='验证损失')
plt.xlabel('训练轮数')
plt.ylabel('MSE损失')
plt.title('训练与验证损失曲线')
plt.legend()
plt.grid(True, alpha=0.3)

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

# -------------------------- 7. 模型保存（保留你的路径） --------------------------
model_path = os.path.join(script_dir, 'danmu_mlp_model.pth')
torch.save(model.state_dict(), model_path)
print(f"\n模型保存路径：{model_path}")