import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import os

plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 最小二乘法的代码实现,这并非自己编写,AI生成的,我在演算纸上纯数学推导了一遍
class MyMultiVarLeastSquares:
    def __init__(self):
        self.beta = None  # 存储参数：beta = [beta0, beta1, beta2, beta3, beta4]^T
        # beta0=截距，beta1~beta4对应4个特征的系数（多变量参数个数=特征数+1）
    
    def fit(self, X, y):
        """
        拟合多变量模型：通过正规方程求解参数
        X: 训练特征矩阵（n×k，k=4个特征）
        y: 训练目标变量（n×1）
        """
        n = len(X)
        # 给X添加常数项列（n×4 → n×5），对应截距beta0（第一列全为1）
        X_with_const = np.hstack([np.ones((n, 1)), X])  # 多变量特征矩阵+常数项
        
        # 正规方程核心步骤（矩阵运算，兼容任意k个特征）
        X_T = X_with_const.T  # X^T：(k+1)×n（此处k=4 → 5×506）
        X_T_X = X_T @ X_with_const  # X^T X：(k+1)×(k+1)（5×5矩阵）
        X_T_y = X_T @ y  # X^T y：(k+1)×1（5×1矩阵）
        
        # 求解逆矩阵（实际应用需处理奇异矩阵，波士顿数据满足可逆条件）
        X_T_X_inv = np.linalg.inv(X_T_X)
        
        # 得到多变量参数beta（5×1矩阵：截距+4个特征系数）
        self.beta = X_T_X_inv @ X_T_y # 这样是直接生成一个可用的beta

    
    def predict(self, X):
        """预测：输入多特征矩阵X（n×4），输出预测值y_hat（n×1）"""
        n = len(X)
        X_with_const = np.hstack([np.ones((n, 1)), X])  # 统一添加常数项
        return X_with_const @ self.beta  # 矩阵乘法：y_hat = X·beta
    

# 彻底对task1进行代码的复用---找另一个文件的位置
data_file = "housing.data"
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, data_file)

# 读取数据,这里先给特征命名
feature_names = [
    "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE",
    "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"
]
# 作用：读取文本文件（.csv 或类似文本格式）并返回 DataFrame。
# Boston成为了DataFrame类的对象了
# 核心表格型数据结构
boston = pd.read_csv(
    file_path,#打开哪里的文件
    sep=r"\s+", # 读取方法sep（全称 separator）指定文件的「字段分隔符」（即数据中列与列之间的分隔方式）。
    
    # 这句话给每一行数据都起了个名字,不用原本列表名字了
    names=feature_names + ["MEDV"] # 列表拼接操作单纯拼一个列表上去
)

# 选择n个核心特征（可根据需要增减）
select_features = [
    "CRIM", "ZN", "INDUS", "CHAS", "NOX", "B"]

X = boston[select_features].values  # 多特征矩阵：shape=(506, 4)
# values,属性 加上 .values 后，会把这个 DataFrame 直接转换成 numpy 数组（ndarray）
y = boston["MEDV"].values.reshape(-1, 1)  # 目标变量转为n×1矩阵（适配矩阵运算）

# 验证数据读取成功
print(f"成功读取本地文件：{file_path}")
print(f"数据集信息：样本数={X.shape[0]}，特征数={X.shape[1]}（多变量）")
print(f"选择的特征：{select_features}")

# 划分训练集和测试集.逻辑与之前一致
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)



# 最小二乘运算
my_model = MyMultiVarLeastSquares()
my_model.fit(X_train, y_train)

y_test_pred = my_model.predict(X_test)

# 6. 输出核心结果（方程+评估指标）
print("多变量线性回归方程：")
print(f"房价 = {my_model.beta[0][0]:.2f} " + 
      " + ".join([f"{my_model.beta[i][0]:.2f}×{select_features[i-1]}" for i in range(1, 5)]))
print(f"测试集R²：{r2_score(y_test, y_test_pred):.2f}")

# 7. 最少必要图：真实值vs预测值（核心拟合效果展示）
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(y_train, y_train, alpha=0.6, color="red",label ='训练集(真实分数)' )
ax.scatter(y_test, y_test_pred, alpha=0.6, color="purple",label = '测试集（真实分数）')  # 散点图
# 理想拟合线（y=x，真实值=预测值）
min_val = min(y_test.min(), y_test_pred.min())
max_val = max(y_test.max(), y_test_pred.max())
ax.plot([min_val, max_val], [min_val, max_val], "black", linewidth=2)
# 图表标注（必须，说明图的含义）
ax.set_xlabel("真实房价（千美元）")
ax.set_ylabel("预测房价（千美元）")
ax.set_title(f"多变量线性回归拟合结果（R²={r2_score(y_test, y_test_pred):.2f}）")


plt.tight_layout()
plt.show()
