import numpy as np

# make a feature = 3 ;
w1 = np.array(1,2,3)
# when function . Firstly thought in\output
# 其中b也是一个nump数组向量
def relu(z):
    a = np.max(z,0)

    return a

def dense(a_in,W,b):
    units = W.shape[1]
    a_out = np.zeros(units)
    for i in range(units):
        w_i = W[:,i]# 取出第几列
        '''
        W = ([[11,12,13],
              [21,22,23]])
              每一列11,21代表一个神经元的权重
        '''
        z = np.dot(w_i,a_in) + b[i]
        a_out[i] = relu(z)

    return a_out
'''
def Sequential(x):
    layer_1 = dense(x,W1,b1)



    return a 
    
'''
W = ([[11,12,13],
    [21,22,23]])
B = np.array([[1,2,3]])
# 不必一个一个取
a = np.array([[1,2,3]])

# 或者
a_vector = np.array([1,2,3])
a = a.T
def vector_dense(a,W,B):
    z = a @ W + B
    out = relu(z)
    return out
