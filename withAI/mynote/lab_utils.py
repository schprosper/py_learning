# 这个东西必须同目录！！！
"""
吴恩达机器学习/深度学习课程配套 lab_utils.py 绘图工具库（复刻版）
核心功能：单变量/多变量线性回归相关可视化（数据散点图、拟合线、成本等高线、梯度下降轨迹）
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# -------------------------- 全局设置（避免中文乱码、统一风格）--------------------------
plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文
plt.rcParams['axes.unicode_minus'] = False    # 支持负号
plt.style.use('seaborn-v0_8-whitegrid')        # 绘图风格（贴近课程）

# -------------------------- 1. 绘制单变量训练数据散点图 --------------------------
def plot_data(x, y, xlabel="特征 X", ylabel="标签 Y", title="训练数据", figsize=(8, 5)):
    """
    绘制单变量线性回归的训练数据散点图
    参数:
        x: 一维数组 (m,)，特征数据（如房屋面积）
        y: 一维数组 (m,)，标签数据（如房屋价格）
        xlabel/ylabel: 坐标轴标签
        title: 图表标题
        figsize: 图表大小
    """
    plt.figure(figsize=figsize)
    plt.scatter(x, y, color='#1f77b4', s=50, alpha=0.7, edgecolors='black', linewidth=0.5)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, pad=15)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -------------------------- 2. 绘制数据+线性拟合线 --------------------------
def plot_linear_fit(x, y, w, b, xlabel="特征 X", ylabel="标签 Y", title="线性回归拟合结果"):
    """
    同时绘制训练数据和拟合线（单变量线性回归：y = w*x + b）
    参数:
        x, y: 训练数据（一维数组）
        w, b: 模型参数（标量）
    """
    plt.figure(figsize=(8, 5))
    # 绘制数据散点
    plt.scatter(x, y, color='#1f77b4', s=50, alpha=0.7, edgecolors='black', linewidth=0.5, label='训练数据')
    # 绘制拟合线（用密集的x值生成平滑直线）
    x_plot = np.linspace(x.min(), x.max(), 100)  # 覆盖x的所有范围
    y_plot = w * x_plot + b
    plt.plot(x_plot, y_plot, color='#ff7f0e', linewidth=2.5, label=f'拟合线: y = {w:.2f}x + {b:.2f}')
    # 图表美化
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=14, pad=15)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -------------------------- 3. 绘制成本函数 J(w,b) 的等高线图 --------------------------
def plot_cost_contour(x, y, compute_cost, w_range=[-10, 10], b_range=[-10, 10], num_points=100):
    """
    绘制成本函数 J(w,b) 的等高线图（直观展示凸函数特性）
    参数:
        x, y: 训练数据
        compute_cost: 成本函数（需提前定义，如之前的 compute_cost）
        w_range/b_range: w和b的取值范围
        num_points: 网格密度（越大越平滑）
    """
    # 生成w和b的网格
    w = np.linspace(w_range[0], w_range[1], num_points)
    b = np.linspace(b_range[0], b_range[1], num_points)
    W, B = np.meshgrid(w, b)  # 生成二维网格

    # 计算每个(w,b)对应的成本J
    J = np.zeros_like(W)
    for i in range(num_points):
        for j in range(num_points):
            J[i, j] = compute_cost(x, y, W[i, j], B[i, j])

    # 绘制等高线
    plt.figure(figsize=(8, 6))
    contour = plt.contour(W, B, J, levels=20, cmap='viridis')  # 20条等高线
    plt.clabel(contour, inline=True, fontsize=8, fmt='%.2f')  # 标注等高线数值
    plt.colorbar(contour, label='成本 J(w,b)')
    plt.xlabel('参数 w', fontsize=12)
    plt.ylabel('参数 b', fontsize=12)
    plt.title('成本函数 J(w,b) 等高线图', fontsize=14, pad=15)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -------------------------- 4. 绘制梯度下降轨迹（等高线+轨迹） --------------------------
def plot_gd_trajectory(x, y, compute_cost, w_history, b_history, w_range=[-10, 10], b_range=[-10, 10]):
    """
    绘制梯度下降过程中参数(w,b)的更新轨迹（在等高线图上叠加轨迹）
    参数:
        w_history: 梯度下降过程中w的所有历史值（数组）
        b_history: 梯度下降过程中b的所有历史值（数组）
    """
    # 先绘制等高线背景
    num_points = 100
    w = np.linspace(w_range[0], w_range[1], num_points)
    b = np.linspace(b_range[0], b_range[1], num_points)
    W, B = np.meshgrid(w, b)
    J = np.zeros_like(W)
    for i in range(num_points):
        for j in range(num_points):
            J[i, j] = compute_cost(x, y, W[i, j], B[i, j])

    # 绘制等高线+轨迹
    plt.figure(figsize=(8, 6))
    contour = plt.contour(W, B, J, levels=20, cmap='viridis', alpha=0.7)
    plt.clabel(contour, inline=True, fontsize=8, fmt='%.2f')
    plt.colorbar(contour, label='成本 J(w,b)')

    # 绘制梯度下降轨迹（散点+连线）
    plt.plot(w_history, b_history, 'r-o', linewidth=2, markersize=6, 
             label='梯度下降轨迹', markerfacecolor='white', markeredgewidth=2)
    # 标注起点和终点
    plt.scatter(w_history[0], b_history[0], color='red', s=100, zorder=5, label=f'起点 (w={w_history[0]:.2f}, b={b_history[0]:.2f})')
    plt.scatter(w_history[-1], b_history[-1], color='green', s=100, zorder=5, label=f'终点 (w={w_history[-1]:.2f}, b={b_history[-1]:.2f})')

    plt.xlabel('参数 w', fontsize=12)
    plt.ylabel('参数 b', fontsize=12)
    plt.title('梯度下降参数更新轨迹', fontsize=14, pad=15)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# -------------------------- 5. 绘制成本随迭代次数的变化 --------------------------
def plot_cost_history(iterations, cost_history, title="成本随迭代次数变化"):
    """
    绘制梯度下降过程中成本J的收敛曲线（验证是否收敛）
    参数:
        iterations: 迭代次数（数组，如 [0,1,2,...,n-1]）
        cost_history: 每次迭代的成本值（数组）
    """
    plt.figure(figsize=(8, 5))
    plt.plot(iterations, cost_history, 'b-', linewidth=2)
    plt.xlabel('迭代次数', fontsize=12)
    plt.ylabel('成本 J(w,b)', fontsize=12)
    plt.title(title, fontsize=14, pad=15)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()