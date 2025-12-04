import copy, math
import numpy as np
import matplotlib.pyplot as plt
import sys
lab_utils_path = r'D:\lpy\mynote'
if lab_utils_path not in sys.path:
    sys.path.append(lab_utils_path)
np.set_printoptions(precision=2)  # 降低numpy数组的显示精度


X_train = np.array([[2104, 5, 1, 45], [1416, 3, 2, 40], [852, 2, 1, 35]])
y_train = np.array([460, 232, 178])

# 数据存储在numpy数组/矩阵中
print(f"X Shape: {X_train.shape}, X Type:{type(X_train)})")
print(X_train)
print(f"y Shape: {y_train.shape}, y Type:{type(y_train)})")
print(y_train)
# 初始值设置
b_init = 785.1811367994083
w_init = np.array([ 0.39133535, 18.75376741, -53.36032453, -26.42131618])
print(f"w_init shape: {w_init.shape}, b_init type: {type(b_init)}")
# 计算f（x）
def predict(x, w, b): 
    """
    single predict using linear regression
    Args:
      x (ndarray): Shape (n,) example with multiple features
      w (ndarray): Shape (n,) model parameters   
      b (scalar):             model parameter 
      
    Returns:
      p (scalar):  prediction
    """
    p = np.dot(x, w) + b     
    return p    
# 从我们的训练数据中获取一行
x_vec = X_train[0,:]# 第0行
print(f"x_vec shape {x_vec.shape}, x_vec value: {x_vec}")

# 预测f值
f_wb = predict(x_vec,w_init, b_init)
print(f"f_wb shape {f_wb.shape}, prediction: {f_wb}")
# 损失函数
def compute_cost(X, y, w, b): 
    """
    compute cost
    Args:
      X (ndarray (m,n)): Data, m examples with n features
      y (ndarray (m,)) : target values
      w (ndarray (n,)) : model parameters  
      b (scalar)       : model parameter
      
    Returns:
      cost (scalar): cost
    """
    m = X.shape[0]
    cost = 0.0
    for i in range(m):      
        f_wb_i = np.dot(X[i], w) + b           #(n,)(n,) = 标量 (见 np.dot)
        cost = cost + (f_wb_i - y[i])**2       #标量
    cost = cost / (2 * m)                      #标量   
    return cost

# 使用我们预先选择的最佳参数计算并显示成本
cost = compute_cost(X_train, y_train, w_init, b_init)
print(f'Cost at optimal w : {cost}')
# 计算梯度
def compute_gradient(X, y, w, b): 
    """
    Args:
      X (ndarray (m,n)): 训练数据，m个实例×n个特征（对应之前的X_train）
      y (ndarray (m,)) : 真实标签，m个实例各一个标签（对应y_train）
      w (ndarray (n,)) : 权重参数，n个特征对应n个权重（之前的w）
      b (scalar)       : 偏差参数（之前的b）
      
    Returns:
      dj_dw (ndarray (n,)): w的梯度（每个权重对应一个梯度）
      dj_db (scalar):       b的梯度（一个值）
    """
    # 初始化
    m,n = X.shape           #(例子的数量，特征的数量)
    dj_dw = np.zeros((n,))
    dj_db = 0.  #就是学习率后面那一块
# 成本函数是关于w求导，所以会掉下来x。
    for i in range(m):                             
        err = (np.dot(X[i], w) + b) - y[i]   # 第几个样本，所产生的误差
        for j in range(n):               # 知道了这个训练样本产生的误差之后
            dj_dw[j] = dj_dw[j] + err * X[i, j] #在第i个训练样本的前提下  
                                                 # 改变每个特征的权重的梯度
                                                    #这里不是123维度，扩展到了n维度
        dj_db = dj_db + err                        
    dj_dw = dj_dw / m   #还没有乘以学习率之前的那一部分                             
    dj_db = dj_db / m                                
        
    return dj_db, dj_dw

#计算和显示梯度 
tmp_dj_db, tmp_dj_dw = compute_gradient(X_train, y_train, w_init, b_init)
print(f'dj_db at initial w,b: {tmp_dj_db}')
print(f'dj_dw at initial w,b: \n {tmp_dj_dw}')
num_iters = 100000
def gradient_descent(X, y, w_in, b_in, cost_function, gradient_function, alpha, num_iters): 
# 在这里进行对参数的反复调整
   """
    执行批量梯度下降（Batch Gradient Descent）以学习模型参数θ。
    通过执行num_iters次梯度下降步骤，每次以学习率α更新参数θ（即w和b）。
    
    参数说明（Args）:
      X (ndarray (m,n))   : 训练数据，m个样本，每个样本包含n个特征（特征矩阵）
      y (ndarray (m,))    : 目标值数组，对应m个样本的真实标签
      w_in (ndarray (n,)) : 初始权重参数，n个特征对应n个初始权重
      b_in (scalar)       : 初始偏置参数（单个标量值）
      cost_function       : 成本函数（用于计算当前参数下的模型预测误差）
      gradient_function   : 梯度计算函数（用于计算成本函数对参数的偏导数）
      alpha (float)       : 学习率（控制每次参数更新的步长，影响收敛速度与效果）
      num_iters (int)     : 梯度下降的迭代次数（即执行参数更新的总步数）
      
    返回值（Returns）:
      w (ndarray (n,)) : 更新后的最优权重参数
      b (scalar)       : 更新后的最优偏置参数
      """
    # 一个数组，用于存储每次迭代的成本J和W，主要用于以后的绘图
    J_history = []
    w = copy.deepcopy(w_in)  #避免在函数中修改全局W
    b = b_in
    
    for i in range(num_iters):

        # 计算梯度并更新参数
        dj_db,dj_dw = gradient_function(X, y, w, b)   ##None

        # 使用w、b、alpha和梯度更新参数
        w = w - alpha * dj_dw               ##None
        b = b - alpha * dj_db               ##None
      
        # 在每次迭代中保存成本J
        if i<100000:      # prevent resource exhaustion 
            J_history.append( cost_function(X, y, w, b))

        # 每隔10次就打印一次成本，如果<10，则打印相同次数的迭代
        if i% math.ceil(num_iters / 10) == 0:
            print(f"Iteration {i:4d}: Cost {J_history[-1]:8.2f}   ")
        
    return w, b, J_history #返回最终的w,b和J的历史记录，用于制图

# 初始化参数
initial_w = np.zeros_like(w_init)
initial_b = 0.
# 一些梯度下降的设置
iterations = 1000
alpha = 5.0e-7
# 运行梯度下降法 
w_final, b_final, J_hist = gradient_descent(X_train, y_train, initial_w, initial_b,
                                                    compute_cost, compute_gradient, 
                                                    alpha, iterations)
print(f"b,w found by gradient descent: {b_final:0.2f},{w_final} ")
m,_ = X_train.shape
for i in range(m):
    print(f"prediction: {np.dot(X_train[i], w_final) + b_final:0.2f}, target value: {y_train[i]}")














