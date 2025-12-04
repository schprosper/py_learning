import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# ===================== 1. 配置与本地数据集读取（核心修改：读取已下载的housing.data）=====================
# 设置中文字体
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 读取本地已下载的 housing.data 文件（确保文件和脚本在同一目录，否则修改file_path）
data_file = "housing.data"  # 你已下载的文件名
# 自动获取脚本所在目录，拼接文件路径（避免手动写绝对路径）
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, data_file)

# 验证文件是否存在
if not os.path.exists(file_path):
    raise FileNotFoundError(f"未找到文件：{file_path}\n请确保 housing.data 与脚本在同一目录，或修改 file_path 为正确路径")

# 读取数据集（housing.data 是空格分隔的文本文件）
feature_names_full = [
    "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE",
    "DIS", "RAD", "TAX", "PTRATIO", "B", "LSTAT"
]
boston = pd.read_csv(
    file_path,
    sep=r"\s+",  # 匹配任意多个空格作为分隔符（适配housing.data格式）
    names=feature_names_full + ["MEDV"]  # 13个特征 + 目标变量MEDV（房价）
)

# 多变量核心：选择4个核心特征（可根据需要增减）
select_features = ["RM", "LSTAT", "PTRATIO", "DIS"]  # 4个特征→多变量
X = boston[select_features].values  # 多特征矩阵：shape=(506, 4)
y = boston["MEDV"].values.reshape(-1, 1)  # 目标变量转为n×1矩阵（适配矩阵运算）

# 验证数据读取成功
print(f"成功读取本地文件：{file_path}")
print(f"数据集信息：样本数={X.shape[0]}，特征数={X.shape[1]}（多变量）")
print(f"选择的特征：{select_features}")

# 划分训练集（80%）和测试集（20%）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)

# ===================== 2. 自行编写多变量最小二乘算法（无修改）=====================
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
        self.beta = X_T_X_inv @ X_T_y
    
    def predict(self, X):
        """预测：输入多特征矩阵X（n×4），输出预测值y_hat（n×1）"""
        n = len(X)
        X_with_const = np.hstack([np.ones((n, 1)), X])  # 统一添加常数项
        return X_with_const @ self.beta  # 矩阵乘法：y_hat = X·beta

# ===================== 3. 模型训练与评估（无修改）=====================
# 1. 自行实现的多变量最小二乘
my_model = MyMultiVarLeastSquares()
my_model.fit(X_train, y_train)
my_y_train_pred = my_model.predict(X_train)
my_y_test_pred = my_model.predict(X_test)

# 2. sklearn的多变量线性回归（对比验证）
sk_model = LinearRegression()
sk_model.fit(X_train, y_train)
sk_y_train_pred = sk_model.predict(X_train)
sk_y_test_pred = sk_model.predict(X_test)

# 输出评估结果（多变量系数展示）
print("\n" + "="*80)
print("【自行实现多变量最小二乘】")
print(f"多变量线性方程：")
print(f"房价 = {my_model.beta[0][0]:.2f} " + 
      " + ".join([f"{my_model.beta[i][0]:.2f}×{select_features[i-1]}" for i in range(1, len(select_features)+1)]))
print(f"训练集MSE：{mean_squared_error(y_train, my_y_train_pred):.2f}")
print(f"测试集MSE：{mean_squared_error(y_test, my_y_test_pred):.2f}")
print(f"测试集R²：{r2_score(y_test, my_y_test_pred):.2f}（越接近1拟合越好）")

print("\n" + "="*80)
print("【sklearn LinearRegression（对比验证）】")
print(f"多变量线性方程：")
print(f"房价 = {sk_model.intercept_[0]:.2f} " + 
      " + ".join([f"{sk_model.coef_[0][i]:.2f}×{select_features[i]}" for i in range(len(select_features))]))
print(f"训练集MSE：{mean_squared_error(y_train, sk_y_train_pred):.2f}")
print(f"测试集MSE：{mean_squared_error(y_test, sk_y_test_pred):.2f}")
print(f"测试集R²：{r2_score(y_test, sk_y_test_pred):.2f}")
print("="*80)

# ===================== 4. 多变量可视化（无修改）=====================
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle("多变量线性回归拟合结果分析（波士顿房价）", fontsize=16)

# —— 子图1：测试集残差图（诊断拟合效果）——
residuals = y_test - my_y_test_pred  # 残差=真实值-预测值
axes[0, 0].scatter(my_y_test_pred, residuals, alpha=0.6, color="steelblue")
axes[0, 0].axhline(y=0, color="red", linestyle="--", linewidth=2)  # 残差为0的参考线
axes[0, 0].set_xlabel("预测房价（千美元）")
axes[0, 0].set_ylabel("残差（真实值-预测值）")
axes[0, 0].set_title("残差图（理想：残差随机分布在0附近）")
axes[0, 0].grid(alpha=0.3)

# —— 子图2：RM（平均房间数）部分依赖图（固定其他特征，看单个特征影响）——
# 固定其他特征为训练集均值
X_mean = X_train.mean(axis=0)  # 4个特征的均值
rm_idx = select_features.index("RM")  # 获取RM在特征列表中的索引
rm_range = np.linspace(X[:, rm_idx].min(), X[:, rm_idx].max(), 100).reshape(-1, 1)  # RM的取值范围
# 构造固定其他特征、仅RM变化的测试矩阵
X_partial_rm = np.tile(X_mean, (100, 1))  # 100×4（全为均值）
X_partial_rm[:, rm_idx] = rm_range.flatten()  # 仅替换RM列
y_partial_rm = my_model.predict(X_partial_rm)  # 预测房价
axes[0, 1].scatter(X_test[:, rm_idx], y_test, alpha=0.5, color="lightcoral", label="测试集真实数据")
axes[0, 1].plot(rm_range, y_partial_rm, color="orange", linewidth=2, label="RM部分依赖线")
axes[0, 1].set_xlabel("平均房间数（RM）")
axes[0, 1].set_ylabel("房价（千美元）")
axes[0, 1].set_title("RM特征部分依赖图（其他特征固定为均值）")
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

# —— 子图3：LSTAT（低收入人口占比）部分依赖图 ——
lstat_idx = select_features.index("LSTAT")  # 获取LSTAT的索引
lstat_range = np.linspace(X[:, lstat_idx].min(), X[:, lstat_idx].max(), 100).reshape(-1, 1)
X_partial_lstat = np.tile(X_mean, (100, 1))
X_partial_lstat[:, lstat_idx] = lstat_range.flatten()
y_partial_lstat = my_model.predict(X_partial_lstat)
axes[1, 0].scatter(X_test[:, lstat_idx], y_test, alpha=0.5, color="lightgreen", label="测试集真实数据")
axes[1, 0].plot(lstat_range, y_partial_lstat, color="darkgreen", linewidth=2, label="LSTAT部分依赖线")
axes[1, 0].set_xlabel("低收入人口占比（LSTAT）")
axes[1, 0].set_ylabel("房价（千美元）")
axes[1, 0].set_title("LSTAT特征部分依赖图（其他特征固定为均值）")
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)

# —— 子图4：真实值vs预测值散点图（整体拟合效果）——
axes[1, 1].scatter(y_test, my_y_test_pred, alpha=0.6, color="purple")
# 理想拟合线（y=x）
min_val, max_val = min(y_test.min(), my_y_test_pred.min()), max(y_test.max(), my_y_test_pred.max())
axes[1, 1].plot([min_val, max_val], [min_val, max_val], "red", linestyle="--", linewidth=2)
axes[1, 1].set_xlabel("真实房价（千美元）")
axes[1, 1].set_ylabel("预测房价（千美元）")
axes[1, 1].set_title(f"真实值vs预测值（R²={r2_score(y_test, my_y_test_pred):.2f}）")
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.show()