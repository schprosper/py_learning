import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False
class ManualLinearRegression:
    """手动实现的线性回归（梯度下降法）"""
    
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations # 循环n_iterations次 = 执行n_iterations次迭代
        self.w = None  # 权重
        self.b = None  # 偏置
        self.loss_history = []  # 记录损失函数历史
    
    def compute_loss(self, X, y):
        """计算均方误差损失"""
        y_pred = self.w * X + self.b    
        return np.mean((y - y_pred) ** 2)#均方误差（MSE）：
    
    def fit(self, X, y):
        """使用梯度下降法训练模型"""
        n_samples = len(X)
        
        # 初始化参数
        self.w = 0
        self.b = 0
        self.loss_history = []
        
        # 梯度下降迭代
        for i in range(self.n_iterations):
            # 计算预测值
            y_pred = self.w * X + self.b
            
            # 计算梯度
            dw = (-2 / n_samples) * np.sum(X * (y - y_pred))
            db = (-2 / n_samples) * np.sum(y - y_pred)
            
            # 更新参数
            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db
            
            # 记录损失
            loss = self.compute_loss(X, y)
            self.loss_history.append(loss)
    
    def predict(self, X):
        """预测"""
        return self.w * X + self.b

def create_synthetic_data():
    """创建合成数据"""
    np.random.seed(42)
    X = np.linspace(0, 10, 100)
    y = 2.5 * X + 1.5 + np.random.normal(0, 1, 100)
    return X, y

def visualize_gradient_descent():
    """可视化梯度下降过程"""
    X, y = create_synthetic_data()
    
    # 不同学习率的实验
    learning_rates = [0.001, 0.01, 0.1, 0.5]
    colors = ['red', 'blue', 'green', 'orange']
    
    plt.figure(figsize=(15, 10))
    
    # 子图1：不同学习率的损失函数收敛情况
    plt.subplot(2, 2, 1)
    for i, lr in enumerate(learning_rates):#第一个获取,这是第几个图,第二个获取学习率
        model = ManualLinearRegression(learning_rate=lr, n_iterations=1000)#这里之后可以创造一个接口
        
        model.fit(X, y)
        plt.plot(range(len(model.loss_history)), model.loss_history, 
                color=colors[i], linewidth=2, label=f'α={lr}')
        print(f"学习率 {lr}: 最终损失 = {model.loss_history[-1]:.4f}, w={model.w:.3f}, b={model.b:.3f}")
    
    plt.xlabel('迭代次数')
    plt.ylabel('损失函数')
    plt.title('不同学习率对损失函数的影响')
    plt.legend()
    plt.grid(True, alpha=0.3)
    #plt.yscale('log')
    
    # 子图2：参数w的变化轨迹
    plt.subplot(2, 2, 2)
    for i, lr in enumerate(learning_rates):
        model = ManualLinearRegression(learning_rate=lr, n_iterations=100)
        w_history = []
        b_history = []
        
        # 重新训练并记录参数历史
        n_samples = len(X)
        w, b = 0, 0
        
        for iteration in range(100):
            y_pred = w * X + b
            dw = (-2 / n_samples) * np.sum(X * (y - y_pred))
            db = (-2 / n_samples) * np.sum(y - y_pred)
            w -= lr * dw
            b -= lr * db
            w_history.append(w)
        
        plt.plot(range(len(w_history)), w_history, color=colors[i], linewidth=2, label=f'α={lr}')
    
    plt.axhline(y=2.5, color='black', linestyle='--', alpha=0.5, label='真实值 w=2.5')
    plt.xlabel('迭代次数')
    plt.ylabel('权重 w')
    plt.title('权重 w 的变化轨迹')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 子图3：参数b的变化轨迹
    plt.subplot(2, 2, 3)
    for i, lr in enumerate(learning_rates):
        model = ManualLinearRegression(learning_rate=lr, n_iterations=100)
        w_history = []
        b_history = []
        
        # 重新训练并记录参数历史
        n_samples = len(X)
        w, b = 0, 0
        
        for iteration in range(100):
            y_pred = w * X + b
            dw = (-2 / n_samples) * np.sum(X * (y - y_pred))
            db = (-2 / n_samples) * np.sum(y - y_pred)
            w -= lr * dw
            b -= lr * db
            b_history.append(b)
        
        plt.plot(range(len(b_history)), b_history, color=colors[i], linewidth=2, label=f'α={lr}')
    
    plt.axhline(y=1.5, color='black', linestyle='--', alpha=0.5, label='真实值 b=1.5')
    plt.xlabel('迭代次数')
    plt.ylabel('偏置 b')
    plt.title('偏置 b 的变化轨迹')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 子图4：最终拟合结果比较
    plt.subplot(2, 2, 4)
    plt.scatter(X, y, alpha=0.6, color='gray', label='数据点')
    
    for i, lr in enumerate(learning_rates):
        model = ManualLinearRegression(learning_rate=lr, n_iterations=1000)
        model.fit(X, y)
        y_pred = model.predict(X)
        plt.plot(X, y_pred, color=colors[i], linewidth=2, label=f'α={lr}')
    
    plt.xlabel('X')
    plt.ylabel('y')
    plt.title('不同学习率的拟合结果')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def analyze_learning_rate_effects():
    """深入分析学习率的影响"""
    X, y = create_synthetic_data()
    
    # 测试更广泛的学习率范围
    learning_rates = [0.0001, 0.001, 0.01, 0.05, 0.1, 0.5, 1.0]
    final_losses = []
    convergence_speeds = []  # 收敛到最终损失90%所需的迭代次数
    
    for lr in learning_rates:
        model = ManualLinearRegression(learning_rate=lr, n_iterations=1000)
        model.fit(X, y)
        final_losses.append(model.loss_history[-1])
        
        # 计算收敛速度：达到最终损失90%所需的迭代次数
        target_loss = model.loss_history[-1] * 1.1  # 最终损失的110%
        for i, loss in enumerate(model.loss_history):
            if loss <= target_loss:
                convergence_speeds.append(i)
                break
        else:
            convergence_speeds.append(1000)  # 未收敛
    
    # 绘制学习率与最终损失的关系
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.semilogx(learning_rates, final_losses, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('学习率 α')
    plt.ylabel('最终损失')
    plt.title('学习率与最终损失的关系')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.semilogx(learning_rates, convergence_speeds, 'ro-', linewidth=2, markersize=8)
    plt.xlabel('学习率 α')
    plt.ylabel('收敛所需迭代次数')
    plt.title('学习率与收敛速度的关系')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("手动实现梯度下降法进行线性回归")
    print("=" * 50)
    
    # 可视化梯度下降过程
    visualize_gradient_descent()
    
    # 分析学习率影响
    analyze_learning_rate_effects()