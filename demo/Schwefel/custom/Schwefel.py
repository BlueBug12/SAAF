import _sa
import random
import numpy as np
import sys


class CustomClass():
    def __init__(self,nVar,x_min,x_max):
        self.n_var = nVar
        self.state = np.zeros(self.n_var)
        self.saved_state = np.zeros(self.n_var)
        self.x_min = x_min[:]
        self.x_max = x_max[:]
        self.best_state = np.zeros(self.n_var)

        for i in range(self.n_var):
            self.state[i] = random.uniform(self.x_min[i],self.x_max[i])

    
    def jumpState(self,scale,cur_t, iter):
        self.saved_state = np.copy(self.state)
        index = random.randint(0,self.n_var-1)
        self.state[index] = self.state[index] + scale*(self.x_max[index]-self.x_min[index])*random.normalvariate(0,1)
        self.state[index] = max(min(self.state[index],self.x_max[index]),self.x_min[index])
    
    def reverse(self):
        self.state = np.copy(self.saved_state)

    def storeBest(self):
        self.best_state = np.copy(self.state)

    def getEnergy(self)->float:
        sum_ = 0.0
        for i in range(self.n_var):
            sum_ += self.state[i]*np.sin(np.sqrt(abs(self.state[i])))
        return 418.9829*self.n_var - sum_

    def output(self):
        print(self.best_state)
        
        
    def stopCondition(self,final_t,energy,cur_t,iter,ag_r,ab_r,rb_r,best_e)->bool:
        return cur_t < final_t

