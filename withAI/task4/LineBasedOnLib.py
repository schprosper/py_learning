import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score

np.random.seed(425)
X = np.random.uniform(low=1,high=10,size=200)
# 自己构造一个函数,然后自己加入噪声
y_true = 8*X + 20 
y = y_true +np.random.normal(loc=0,scale=5,size=200)

# NumPy 数组（numpy.ndarray）的内置方法,必须必须用他的数组(矩阵)
X = X.reshape(-1,1)
# sklearn兼容numpy

X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size = 0.2,random_state=423
)

model = LinearRegression()
# 面向对象编程
# 很方便自己寻找,自己生成
model.fit(X_train,y_train)
# 得到一下高中所说的y估计
y_train_pred = model.predict(X_train)#训练集用拟合的函数,生成训练集的预测值
y_test_pred = model.predict(X_test)

print(f"训练得到的线性方程：y = {model.coef_[0]}x + {model.intercept_}")
print(f"真实线性方程：y = 8x + 20")
print(f"测试集均方误差（MSE）：{mean_squared_error(y_test, y_test_pred)}")
print(f"测试集决定系数（R²）：{r2_score(y_test, y_test_pred)}") 
# 先生成背景
plt.figure(figsize=(10,6))
# 散点图
plt.scatter(X_train,y_train,color = 'blue',alpha=0.8,label='训练集(真实分数)')
plt.scatter(X_test,y_test,color = 'red',alpha=0.8,label = '测试集（真实分数）')

# 拟合曲线,
X_full = np.linspace(1, 10, 100).reshape(-1, 1)
y_full_pred = model.predict(X_full)
plt.plot(X_full, y_full_pred, color='orange', linewidth=3, label=f'拟合直线：y={model.coef_[0]:.2f}x+{model.intercept_:.2f}')

plt.xlabel('学习时长',fontsize = 12)
plt.ylabel('考试分数（分）', fontsize=12)
plt.title('学习时长与考试分数的线性回归分析', fontsize=14)
plt.legend()  # 显示图例
plt.show()  # 弹出图片