import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

class ManualLinearRegression:

    def __init__(self,learning_rate = 0.01,n_iterations = 1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.w = None
        self.b = None
        self.loss_history= []
        self.w_history =[]
        self.b_history = []

    def compute_loss(self, X, y):# x,y传入一维列表
        y_pred = self.w * X + self.b   
        return np.mean((y - y_pred) ** 2) # 均方误差
    
    def fit(self,X,y):

        n_samples = len(X)

        self.w = 0
        self.b = 0
        self.loss_history = []


        for i in range(self.n_iterations):
            y_pred = self.w * X + self.b

            dw = (-2 / n_samples) * np.sum(X * (y - y_pred))
            db = (-2 / n_samples) * np.sum(y - y_pred)

            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db

             # 记录w和b的历史值
            self.w_history.append(self.w)
            self.b_history.append(self.b)
             # 记录损失
            loss = self.compute_loss(X, y)
            self.loss_history.append(loss)

    def predict(self,X):
        return self.w * X + self.b
    

def create_synthethic_data():
    '''合成训练数据'''
    np.random.seed(452)
    X = np.linspace(0,10,100)
    y = 2.5 * X +1.5 + np.random.normal(0,1,100)
    return X,y


def visualize_gradient_descent():
    # 首先,这里是可视化要求,所以必须先导入一下X和y的数据
    # 如果在这里不去导入,那就得在可视化函数里面留一下接口了
    '''
    self,
    '''
    X,y = create_synthethic_data()

    learning_rates = [0.001,0.01,0.1,0.5]
    colors = ['red', 'blue', 'green', 'orange']

    plt.figure(figsize=(15,10))

    # 不同学习率的损失函数收敛情况
    plt.subplot(2, 2, 1)
    for i, lr in enumerate(learning_rates):
        model = ManualLinearRegression(learning_rate=lr, n_iterations=1000)#这里之后可以创造一个接口
        
        model.fit(X, y)# 调用写出的fit函数(改变w和b的属性)
        plt.plot(range(len(model.loss_history)), model.loss_history, 
                color=colors[i], linewidth=2, label=f'α={lr}')
        print(f"学习率 {lr}: 最终损失 = {model.loss_history[-1]:.4f}, w={model.w:.3f}, b={model.b:.3f}")
    
    plt.xlabel('迭代次数')
    plt.ylabel('损失函数')
    plt.title('不同学习率对损失函数的影响')
    plt.legend()
    plt.grid(True, alpha=0.3)
    #plt.yscale('log')



    # ：参数w的变化轨迹
    plt.subplot(2, 2, 2)
    for i, lr in enumerate(learning_rates):
        model = ManualLinearRegression(learning_rate=lr, n_iterations=100)
        model.fit(X, y)
        plt.plot(range(len(model.w_history)), model.w_history, color=colors[i], linewidth=2, label=f'α={lr}')
    
    plt.axhline(y=2.5, color='black', linestyle='--', alpha=0.5, label='真实值 w=2.5')
    plt.xlabel('迭代次数')
    plt.ylabel('权重 w')
    plt.title('权重 w 的变化轨迹')
    plt.legend()
    plt.grid(True, alpha=0.3)


    plt.plot(range(i),model.w_history)


# 参数b的变化轨迹
# 逻辑和2几乎一样
    plt.subplot(2, 2, 3)
    for i, lr in enumerate(learning_rates):
        model = ManualLinearRegression(learning_rate=lr, n_iterations=100)
        model.fit(X, y)
        
        plt.plot(range(len(model.b_history)), model.b_history, color=colors[i], linewidth=2, label=f'α={lr}')
    
    plt.axhline(y=1.5, color='black', linestyle='--', alpha=0.5, label='真实值 b=1.5')
    plt.xlabel('迭代次数')
    plt.ylabel('偏置 b')
    plt.title('偏置 b 的变化轨迹')
    plt.legend()
    plt.grid(True, alpha=0.3)

# 最终拟合结果比较
    plt.subplot(2, 2, 4)
    plt.scatter(X, y, alpha=0.6, color='gray', label='数据点')
    
    for i, lr in enumerate(learning_rates):# 提取学习率然后分别生成线性回归图
        model = ManualLinearRegression(learning_rate=lr, n_iterations=1000)
        model.fit(X, y)
        y_pred = model.predict(X)
        plt.plot(X, y_pred, color=colors[i], linewidth=2, label=f'α={lr}')
    
    plt.xlabel('X')
    plt.ylabel('y')
    plt.title('不同学习率的拟合结果')
    plt.legend()
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("手动实现梯度下降法进行线性回归")
    print("=" * 50)
    
    # 可视化梯度下降过程
    visualize_gradient_descent()
    
