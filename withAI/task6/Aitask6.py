import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # 允许重复加载 OpenMP 库（规避报错）
os.environ["OMP_NUM_THREADS"] = "4" 

import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
# 数据预处理
# transforms.Compose: 将多个数据变换操作组合成一个序列
transform = transforms.Compose([
    transforms.ToTensor(),  # 将PIL图像或numpy数组转换为PyTorch张量，同时将像素值从[0,255]自动归一化到[0,1]
    transforms.Normalize((0.1307,), (0.3081,))  # 对图像进行标准化，使用MNIST数据集的均值和标准差
    # 标准化公式: (x - mean) / std，这里x∈[0,1]，标准化后分布更接近正态分布，有助于模型训练
])

# MNIST数据集加载
# datasets.MNIST: PyTorch内置的MNIST数据集类
# root: 数据集存储路径；train: True为训练集，False为测试集；download: 如果本地不存在则下载
train_dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_dataset = datasets.MNIST(root="./data", train=False, download=True, transform=transform)

# DataLoader: 数据加载器，负责批量加载数据、打乱顺序等
# batch_size: 每个批次的样本数；shuffle: 是否在每个epoch开始时打乱数据顺序
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)  # 训练时打乱顺序避免模型学习到数据顺序
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)  # 测试时不需要打乱

# TODO: 定义CNN模型
class SimpleCNN(nn.Module):
    """
    简单的CNN模型架构：
    输入: [batch_size, 1, 28, 28] (MNIST图像尺寸28x28，单通道灰度图)
    输出: [batch_size, 10] (10个数字类别的预测概率)
    """
    def __init__(self):
        super(SimpleCNN, self).__init__()  # 调用父类nn.Module的构造函数
        
        # 第一个卷积块: Conv1 -> ReLU -> MaxPool
        self.conv1 = nn.Conv2d(
            in_channels=1,      # 输入通道数，灰度图为1
            out_channels=16,    # 输出通道数，即16个卷积核，提取16种特征
            kernel_size=3,      # 卷积核大小3x3
            padding=1           # 边缘填充1像素，保持输出尺寸与输入相同(28x28)
        )
        # 卷积后: [batch_size, 16, 28, 28]
        
        # 第二个卷积块: Conv2 -> ReLU -> MaxPool  
        self.conv2 = nn.Conv2d(
            in_channels=16,     # 输入通道数，来自上一层输出
            out_channels=32,    # 输出通道数，32个卷积核
            kernel_size=3,      # 卷积核大小3x3
            padding=1           # 填充保持尺寸
        )
        # 卷积后: [batch_size, 32, 14, 14]
        
        # 激活函数和池化层
        self.relu = nn.ReLU()   # ReLU激活函数，f(x)=max(0,x)，解决梯度消失，引入非线性
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)  # 最大池化，2x2窗口，步长2，尺寸减半
        
        # 全连接层
        self.fc1 = nn.Linear(32 * 7 * 7, 128)  # 输入: 32*7*7 (经过两次池化后尺寸)，输出: 128个神经元
        self.fc2 = nn.Linear(128, 10)          # 输入: 128，输出: 10个数字类别
        
        # Dropout层用于防止过拟合，在训练时随机丢弃部分神经元
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        """
        前向传播定义数据流动路径
        x: 输入张量 [batch_size, 1, 28, 28]
        返回: 输出张量 [batch_size, 10]
        """
        # 第一个卷积块
        x = self.conv1(x)      # -> [batch_size, 16, 28, 28]
        x = self.relu(x)       # 激活函数，形状不变
        x = self.pool(x)       # 最大池化 -> [batch_size, 16, 14, 14]
        
        # 第二个卷积块  
        x = self.conv2(x)      # -> [batch_size, 32, 14, 14]
        x = self.relu(x)       # 激活函数
        x = self.pool(x)       # 最大池化 -> [batch_size, 32, 7, 7]
        
        # 展平操作: 将多维特征图转换为一维向量，为全连接层准备
        # view()函数重塑张量形状，-1表示自动计算该维度大小
        x = x.view(-1, 32 * 7 * 7)  # -> [batch_size, 32*7*7=1568]
        
        # 全连接层
        x = self.fc1(x)        # -> [batch_size, 128]
        x = self.relu(x)       # 激活函数
        x = self.dropout(x)    # Dropout防止过拟合，只在训练时生效
        x = self.fc2(x)        # -> [batch_size, 10] (10个类别的得分/logits)
        
        return x  # 返回原始得分，CrossEntropyLoss内部会处理softmax

# TODO: 定义训练和验证函数
def train(model, train_loader, criterion, optimizer, device):
    """
    训练函数: 在一个epoch内完成模型训练
    参数:
        model: 神经网络模型
        train_loader: 训练数据加载器  
        criterion: 损失函数
        optimizer: 优化器
        device: 计算设备(CPU/GPU)
    返回:
        avg_loss: 该epoch的平均训练损失
    """
    model.train()  # 设置为训练模式，启用dropout、batch normalization的训练行为
    total_loss = 0.0  # 累计损失
    total_samples = 0  # 总样本数
    
    # 遍历训练数据的所有批次
    for batch_idx, (images, labels) in enumerate(train_loader):
        # 将数据转移到指定设备(CPU/GPU)
        images, labels = images.to(device), labels.to(device)
        
        # 前向传播: 数据通过模型得到预测输出
        outputs = model(images)  # 形状: [batch_size, 10]
        
        # 计算损失: 比较预测输出和真实标签
        loss = criterion(outputs, labels)
        
        # 反向传播和优化
        optimizer.zero_grad()  # 清空梯度: 必须在新批次前清空，否则梯度会累积
        loss.backward()        # 反向传播: 计算损失对模型参数的梯度
        optimizer.step()       # 参数更新: 根据梯度更新模型权重
        
        # 累计统计
        batch_size = images.size(0)  # 当前批次样本数
        total_loss += loss.item() * batch_size  # 累计损失(乘以批次大小)
        total_samples += batch_size  # 累计样本数
        
        # 每100个批次打印一次训练状态
        if batch_idx % 100 == 0:
            print(f'  训练批次 [{batch_idx}/{len(train_loader)}], 当前批次损失: {loss.item():.4f}')
    
    # 计算该epoch的平均训练损失
    avg_loss = total_loss / total_samples
    return avg_loss

def evaluate(model, test_loader, criterion, device):
    """
    验证函数: 在测试集上评估模型性能，不更新参数
    参数:
        model: 神经网络模型
        test_loader: 测试数据加载器
        criterion: 损失函数  
        device: 计算设备
    返回:
        avg_loss: 平均测试损失
        accuracy: 测试准确率(%)
    """
    model.eval()  # 设置为评估模式，禁用dropout、使用训练好的batch normalization统计量
    total_loss = 0.0
    correct = 0    # 正确预测的样本数
    total_samples = 0
    
    # torch.no_grad(): 禁用梯度计算，节省内存和计算资源
    with torch.no_grad():
        for images, labels in test_loader:
            # 数据转移到设备
            images, labels = images.to(device), labels.to(device)
            
            # 前向传播
            outputs = model(images)
            
            # 计算损失
            loss = criterion(outputs, labels)
            
            # 累计损失
            batch_size = images.size(0)
            total_loss += loss.item() * batch_size
            total_samples += batch_size
            
            # 计算准确率
            # torch.max返回(最大值, 最大值索引)，我们只需要索引(预测类别)
            _, predicted = torch.max(outputs.data, 1)  # 在维度1(类别维度)上取最大值
            
            # 统计正确预测的数量
            correct += (predicted == labels).sum().item()  # .item()将张量转换为Python数值
    
    # 计算平均损失和准确率
    avg_loss = total_loss / total_samples
    accuracy = 100.0 * correct / total_samples  # 转换为百分比
    
    return avg_loss, accuracy

# 主训练流程
if __name__ == "__main__":
    # 设置计算设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # 初始化模型
    model = SimpleCNN().to(device)  # 将模型转移到指定设备
    
    # 定义损失函数和优化器
    criterion = nn.CrossEntropyLoss()  # 交叉熵损失，内部包含softmax，适合多分类问题
    optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam优化器，自适应学习率
    
    # 训练参数
    epochs = 2  # 训练轮次
    train_losses = []  # 记录每个epoch的训练损失
    test_losses = []   # 记录每个epoch的测试损失  
    test_accuracies = []  # 记录每个epoch的测试准确率
    
    print("开始训练CNN模型...")
    
    # 训练循环
    for epoch in range(epochs):
        print(f"\nEpoch [{epoch+1}/{epochs}]")
        
        # 训练一个epoch
        train_loss = train(model, train_loader, criterion, optimizer, device)
        
        # 在测试集上评估
        test_loss, test_accuracy = evaluate(model, test_loader, criterion, device)
        
        # 记录训练过程
        train_losses.append(train_loss)
        test_losses.append(test_loss)
        test_accuracies.append(test_accuracy)
        
        # 打印epoch结果
        print(f"Epoch [{epoch+1}/{epochs}] 完成:")
        print(f"  训练损失: {train_loss:.4f}")
        print(f"  测试损失: {test_loss:.4f}") 
        print(f"  测试准确率: {test_accuracy:.2f}%")
    
    # 绘制训练曲线
    plt.figure(figsize=(15, 5))
    
    # 子图1: 损失曲线
    plt.subplot(1, 2, 1)
    plt.plot(range(1, epochs+1), train_losses, 'b-', label='训练损失', linewidth=2)
    plt.plot(range(1, epochs+1), test_losses, 'r-', label='测试损失', linewidth=2)
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.title('训练和测试损失曲线', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # 子图2: 准确率曲线
    plt.subplot(1, 2, 2)
    plt.plot(range(1, epochs+1), test_accuracies, 'g-', label='测试准确率', linewidth=2)
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('准确率 (%)', fontsize=12)
    plt.title('测试准确率曲线', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()  # 自动调整子图间距
    plt.show()
    
    # 最终评估
    final_test_loss, final_test_accuracy = evaluate(model, test_loader, criterion, device)
    print(f"\n{'='*50}")
    print(f"训练完成!")
    print(f"最终测试准确率: {final_test_accuracy:.2f}%")
    print(f"最终测试损失: {final_test_loss:.4f}")
    
    # 过拟合/欠拟合分析
    print(f"\n模型性能分析:")
    
    # 计算训练集和测试集的最终准确率差异
    _, train_accuracy = evaluate(model, train_loader, criterion, device)
    accuracy_gap = train_accuracy - final_test_accuracy
    
    if accuracy_gap > 5:  # 如果训练准确率比测试准确率高5%以上
        print("⚠️  检测到可能过拟合: 训练准确率显著高于测试准确率")
        print(f"   训练准确率: {train_accuracy:.2f}% vs 测试准确率: {final_test_accuracy:.2f}%")
        print("   建议: 增加dropout比率、使用数据增强、减少模型复杂度")
    elif final_test_accuracy < 95:  # 如果测试准确率低于95%
        print("⚠️  检测到可能欠拟合: 模型性能未达到预期")
        print(f"   当前测试准确率: {final_test_accuracy:.2f}%")
        print("   建议: 增加训练轮次、调整学习率、增加模型复杂度")
    else:
        print("✅ 模型训练良好，过拟合和欠拟合风险较低")
        print(f"   训练准确率: {train_accuracy:.2f}%")
        print(f"   测试准确率: {final_test_accuracy:.2f}%")
    
    print(f"{'='*50}")