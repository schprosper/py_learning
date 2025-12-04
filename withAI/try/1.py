import numpy as np
import matplotlib as plt
import random

class My_Linear:# 单个就好
    '''
    要实现完整的线性回归逻辑,不包含参数问题
    '''
    def __init__(self,lr):
        self.w = None
        self.b = None
        self.n_iteration = None
        self.lr = lr
        self.history_loss = []
        self.w_history = []
        self.b_history = []

    def loss(self,x,y):
        y_pred = self.w * x + self.b
        loss = np.mean((y - y_pred)**2)
        return loss
    




    def fit(self,x,y_train):
        n_sample = len(x)

        self.w = 1
        self.b = 1



        for i in range(self.n_iteration):
            y_pred = self.w * x + self.b

            dw = (-2/n_sample)*np.sum(x * (y_train - y_pred))
            db = (-2/n_sample)*np.sum(y_train- y_pred)

            self.w -= self.lr * dw
            self.b -= self.lr * db
            # 记录w和b的历史值
            self.w_history.append(self.w)
            self.b_history.append(self.b)
                # 记录损失
            loss = self.compute_loss(X, y)
            self.loss_history.append(loss)

    def predict(self,x):
        return self.w * x + self.b



def creat_data(self):
    np.random.seed(42)
    x = np.random.uniform(0,1,100)
    y_train = 2.5 * x + 1.2 + np.random.normal(0,1,100)
    return x , y_train

plt.subplot(2, 2, 1)
for i, lr in enumerate(learning_rates):



        









    









if  __file__ == "__main__":
    x = np.random()

    linear = My_Linear (x)
    
        
        