import math                         
import random                     
import numpy as np                  
import matplotlib.pyplot as plt    
from datetime import datetime


class SA:

    def __init__(self,descent_rate: float, initial_t: float, final_t: float, scale: float, x_min, x_max, markov_iter: int, n_var: int):
        self.setParam(descent_rate,initial_t,final_t,scale, x_min,x_max,markov_iter,n_var)

    def setParam(self, descent_rate: float, initial_t: float, final_t: float, scale:float, x_min, x_max, markov_iter: int, n_var: int):
        self.descent_rate = descent_rate
        self.initial_t = initial_t
        self.final_t = final_t
        self.scale = scale

        self.x_min = np.zeros((n_var))
        self.x_max = np.zeros((n_var))

        self.x_min[:] = x_min[:]
        self.x_max[:] = x_max[:]
        self.n_var = 0
        self.energy = 0
        self.markov_iter = markov_iter
        self.e_now_record = []
        self.e_best_record = []
        self.solution =[]
        self.iter_record = []
    
    def setInitialState(self, state):
        self.n_var = len(state)
        self.state = np.zeros(self.n_var)
        self.state[:] = state[:]
        self.energy = self.getEnergy(state)

    def acceptance(self, delta_energy: float, temperature: float):
        return math.exp(-delta_energy/temperature)
    
    def run(self):
        #randseed = random.randint(1,100)
        #random.seed(randseed)
        accept_good = 0
        accept_bad = 0
        reject_bad = 0
        self.num_iter = 0

        cur_t = self.initial_t
        cur_state = np.zeros(self.n_var)
        cur_state[:] = self.state[:]

        new_state = np.zeros(self.n_var)
 
        cur_e = self.getEnergy(cur_state)
        best_e = cur_e
        while cur_t >= self.final_t:
            for k in range(self.markov_iter):
                new_state[:] = self.neighbor(cur_state)
                new_e = self.getEnergy(new_state)
                delta_e = new_e - cur_e
                if delta_e < 0:
                    cur_e = new_e
                    cur_state[:] = new_state[:]
                    accept_good += 1
                    self.scale = self.scale*0.99
                else:
                    prob = self.acceptance(delta_e, cur_t)
                    if prob > random.random():
                        cur_e = new_e
                        cur_state[:] = new_state[:]
                        accept_bad += 1
                    else:
                        reject_bad += 1
                if(best_e > cur_e):
                    best_e = cur_e
                    self.solution[:] = cur_state[:]
            self.e_best_record.append(round(best_e,4))
            self.e_now_record.append(round(cur_e,4))
            self.iter_record.append(self.num_iter)

            cur_t = cur_t*self.descent_rate 
            self.num_iter += 1
        print("final result")
        print("accept good: ",accept_good)
        print("accept bad:", accept_bad)
        print("reject bad:", reject_bad)
        print("solution:",self.solution)
        print("final energy:", cur_t)
        print("iterations",self.num_iter)


    def neighbor(self, state):
        new_state = np.zeros(self.n_var)
        new_state[:] = state[:]
        v = random.randint(0,len(state)-1)
        new_state[v] = state[v] + self.scale*(self.x_max[v]-self.x_min[v])*random.normalvariate(0,1) 
        new_state[v] = max(min(new_state[v],self.x_max[v]),self.x_min[v])
        return new_state

    def getEnergy(self,state):
        sum_ = 0.0
        for i in range(self.n_var):
            sum_ += state[i]*np.sin(np.sqrt(abs(state[i])))
        return 418.9829*self.n_var - sum_

    def plot(self):
        plt.figure(figsize=(6,4),facecolor='#FFFFFF')
        plt.title("result")
        plt.xlim((0,self.num_iter))
        plt.xlabel('iter')
        plt.ylabel('f(x)')
        plt.plot(self.iter_record,self.e_now_record,'b-',label="FxNow")
        plt.plot(self.iter_record,self.e_best_record,'r-',label="FxBest")
        plt.legend()
        plt.show()

def main():
    x_min = [-500,-500]
    x_max = [500,500]
    a = SA(0.98,100.0,1,0.5,x_min,x_max,100,2)
    x_initial = np.zeros(2)
    for v in range(2):
        x_initial[v] = random.uniform(x_min[v],x_max[v])
    a.setInitialState(x_initial)
    a.run()
    a.plot()

if __name__ == '__main__':
    main()
