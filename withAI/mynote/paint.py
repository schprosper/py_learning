import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# --------------------------
# 全局设置（贴合吴恩达课程风格）
# --------------------------
plt.rcParams['figure.figsize'] = (8, 6)  # 图表大小（课程常用尺寸）
plt.rcParams['font.size'] = 10          # 字体大小
plt.rcParams['axes.grid'] = True        # 显示网格（课程图表常见）
plt.rcParams['axes.spines.top'] = False  # 隐藏上边框
plt.rcParams['axes.spines.right'] = False# 隐藏右边框

# --------------------------
# 1. 绘制散点图（分类/回归数据可视化）
# --------------------------
def plot_data(X, y, xlabel='Feature 1', ylabel='Feature 2', 
              pos_label='Positive', neg_label='Negative', 
              title='Data Visualization'):
    """
    吴恩达课程最常用的散点图（适配二分类/回归数据）
    对应场景：逻辑回归入门（如癌症检测、录取预测）的数据分布展示
    参数：
        X: (m, 2) 特征矩阵（2个特征，便于二维可视化）
        y: (m, 1) 标签向量（0/1 二分类，或连续值回归）
        xlabel/ylabel: 坐标轴标签（默认贴合二分类场景）
        pos_label/neg_label: 正负样本标签（默认Positive/Negative）
    """
    # 区分正负样本（二分类）或直接画所有点（回归）
    if len(np.unique(y)) == 2:  # 二分类数据
        pos_mask = (y == 1).flatten()  # 正样本掩码
        neg_mask = (y == 0).flatten()  # 负样本掩码
        
        # 绘制正负样本散点（颜色、标记贴合课程风格）
        plt.scatter(X[pos_mask, 0], X[pos_mask, 1], 
                   c='darkblue', marker='+', s=100, linewidth=2, label=pos_label)
        plt.scatter(X[neg_mask, 0], X[neg_mask, 1], 
                   c='yellow', marker='o', s=80, edgecolors='darkblue', label=neg_label)
    else:  # 回归数据（连续标签）
        plt.scatter(X[:, 0], y, c='darkblue', marker='o', s=60, edgecolors='white')
    
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    if len(np.unique(y)) == 2:
        plt.legend(loc='best')
    plt.show()

# --------------------------
# 2. 绘制代价函数下降曲线（梯度下降收敛性验证）
# --------------------------
def plot_cost_history(J_history, title='Cost Function vs. Iterations'):
    """
    吴恩达课程必用：梯度下降过程中代价函数的变化曲线
    对应场景：验证梯度下降是否收敛（J应逐渐减小并趋于平稳）
    参数：
        J_history: (num_iters,) 数组，记录每次迭代的代价
    """
    iterations = np.arange(1, len(J_history) + 1)  # 迭代次数（从1开始）
    plt.plot(iterations, J_history, c='darkred', linewidth=2)
    plt.xlabel('Number of Iterations', fontsize=12)
    plt.ylabel('Cost J(θ)', fontsize=12)
    plt.title(title, fontsize=14)
    plt.yscale('log')  # 对数坐标（便于观察早期快速下降和后期收敛）
    plt.show()

# --------------------------
# 3. 绘制线性回归拟合曲线
# --------------------------
def plot_linear_regression_fit(X, y, theta, xlabel='X', ylabel='y', title='Linear Regression Fit'):
    """
    线性回归拟合结果可视化（1个特征场景，课程入门必学）
    对应场景：单变量线性回归（如房价预测）的拟合效果展示
    参数：
        X: (m, 1) 特征矩阵（单特征）
        y: (m, 1) 标签向量
        theta: (2, 1) 参数（含偏置项θ₀）
    """
    # 绘制原始数据
    plt.scatter(X[:, 0], y, c='darkblue', marker='o', s=60, edgecolors='white', label='Training Data')
    
    # 绘制拟合直线（取X的最小值和最大值，保证直线覆盖整个数据范围）
    X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)  # 生成均匀点
    X_range_with_intercept = np.hstack((np.ones((100, 1)), X_range))  # 添加偏置项
    y_pred = X_range_with_intercept @ theta  # 预测值（拟合直线）
    
    plt.plot(X_range, y_pred, c='darkred', linewidth=2, label='Linear Fit')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    plt.legend(loc='best')
    plt.show()

# --------------------------
# 4. 绘制逻辑回归决策边界（二分类核心可视化）
# --------------------------
def plot_logistic_decision_boundary(X, y, theta, xlabel='Feature 1', ylabel='Feature 2', title='Decision Boundary'):
    """
    吴恩达逻辑回归重点：绘制二分类的决策边界（线性/非线性通用）
    对应场景：逻辑回归分类结果（如录取预测、微芯片质量检测）
    参数：
        X: (m, 2) 特征矩阵（2个特征，二维决策边界）
        y: (m, 1) 标签向量（0/1）
        theta: (n+1, 1) 参数向量（n=2时为线性决策边界）
    """
    # 先绘制原始数据散点
    plot_data(X, y, xlabel=xlabel, ylabel=ylabel, title=title, show=False)
    
    # 生成网格点（用于绘制决策边界）
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.linspace(x1_min, x1_max, 100),
                           np.linspace(x2_min, x2_max, 100))
    
    # 计算网格点的预测值（决策边界：h(θ)=0.5 → X@θ=0）
    grid = np.c_[np.ones(xx1.ravel().shape), xx1.ravel(), xx2.ravel()]  # 添加偏置项
    Z = (grid @ theta).reshape(xx1.shape)  # 线性决策边界：X@θ=0
    
    # 绘制决策边界（等高线，Z=0即为边界）
    plt.contour(xx1, xx2, Z, levels=[0], colors='darkred', linewidths=2)
    plt.legend(loc='best')
    plt.show()

# --------------------------
# 5. 绘制多项式逻辑回归决策边界（非线性场景）
# --------------------------
def plot_poly_decision_boundary(X, y, theta, poly_features_func, xlabel='Feature 1', ylabel='Feature 2', title='Polynomial Decision Boundary'):
    """
    吴恩达正则化章节重点：多项式逻辑回归的非线性决策边界
    对应场景：微芯片质量检测（非线性特征）
    参数：
        poly_features_func: 函数，输入原始X(2维)，返回多项式特征矩阵（含偏置项）
    """
    # 绘制原始数据散点
    plot_data(X, y, xlabel=xlabel, ylabel=ylabel, title=title, show=False)
    
    # 生成网格点
    x1_min, x1_max = X[:, 0].min() - 0.1, X[:, 0].max() + 0.1
    x2_min, x2_max = X[:, 1].min() - 0.1, X[:, 1].max() + 0.1
    xx1, xx2 = np.meshgrid(np.linspace(x1_min, x1_max, 100),
                           np.linspace(x2_min, x2_max, 100))
    
    # 计算网格点的多项式特征和预测值
    grid_poly = poly_features_func(np.c_[xx1.ravel(), xx2.ravel()])  # 多项式特征
    Z = (grid_poly @ theta).reshape(xx1.shape)
    
    # 绘制非线性决策边界（填充等高线，更直观）
    plt.contourf(xx1, xx2, Z, alpha=0.3, cmap=ListedColormap(['yellow', 'lightblue']))
    plt.contour(xx1, xx2, Z, levels=[0], colors='darkred', linewidths=2)
    plt.legend(loc='best')
    plt.show()

# --------------------------
# 辅助函数：plot_data的内部复用（控制是否立即显示）
# --------------------------
def plot_data(X, y, xlabel='Feature 1', ylabel='Feature 2', 
              pos_label='Positive', neg_label='Negative', 
              title='Data Visualization', show=True):
    """内部复用版本，支持不立即显示（用于叠加决策边界）"""
    if len(np.unique(y)) == 2:
        pos_mask = (y == 1).flatten()
        neg_mask = (y == 0).flatten()
        plt.scatter(X[pos_mask, 0], X[pos_mask, 1], 
                   c='darkblue', marker='+', s=100, linewidth=2, label=pos_label)
        plt.scatter(X[neg_mask, 0], X[neg_mask, 1], 
                   c='yellow', marker='o', s=80, edgecolors='darkblue', label=neg_label)
    else:
        plt.scatter(X[:, 0], y, c='darkblue', marker='o', s=60, edgecolors='white')
    
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14)
    if len(np.unique(y)) == 2:
        plt.legend(loc='best')
    if show:
        plt.show()