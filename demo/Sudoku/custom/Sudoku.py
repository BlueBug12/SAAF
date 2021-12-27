import _sa
import random
import numpy as np
import sys

class CustomClass():
    def __init__(self,filename):
        self.state = self.parser(filename)
        self.none_zero_idx = np.arange(81)[self.state>0]
        self.best_state = np.zeros(81)
        self.swap_idx = [0,0]
        #randomly fill the empty entries
        for num in range(9):
            b_idx = self.get_block_indices(num)
            b_element = self.state[b_idx]
            zero_indices = [idx for i,idx in enumerate(b_idx) if b_element[i]==0]
            to_fill = [i for i in range(1,10) if i not in b_element]
            random.shuffle(to_fill)
            for i in range(len(to_fill)):
                self.state[zero_indices[i]] = to_fill[i]
    
    def get_block_indices(self,b,ignore = False):
        row_base = (b//3)*3
        col_base = (b%3)*3
        indices = [col_base + (i%3) + 9*(row_base+(i//3)) for i in range(9)]
        if ignore:
            indices = list(filter(lambda x:x not in self.none_zero_idx,indices))
        return indices
    
    def parser(self,filename):
        data = [] 
        with open(filename) as f:
            for i in range(9):
                line = f.readline()
                line = line.split()
                line = [int(i) for i in line]
                data += line

        return np.array(data)
        
    
    def get_col_indices(self,col):
        return [col+9*i for i in range(9)]

    def get_row_indixes(slef,row):
        return [i + 9*row for i in range(9)]
    
    def jumpState(self,scale,cur_t, iter):
        block = random.randint(0,8)
        zero_indices = self.get_block_indices(block,ignore=True)
        self.swap_idx = random.sample(zero_indices,2)
        #self.swap_idx = picked_block.copy()
        s1 = self.swap_idx[0]
        s2 = self.swap_idx[1]
        self.state[s1], self.state[s2] = self.state[s2], self.state[s1]

    def reverse(self):
        self.state[self.swap_idx[0]], self.state[self.swap_idx[1]] = self.state[self.swap_idx[1]], self.state[self.swap_idx[0]]

    def storeBest(self):
        self.best_state = np.copy(self.state)

    def getEnergy(self)->float:
        score = 0
        for row in range(9):
            score -= len(set(self.state[self.get_row_indixes(row)]))
        for col in range(9):
            score -= len(set(self.state[self.get_col_indices(col)]))
        return score

    def output(self):
        pass
        
    def stopCondition(self,final_t,energy,cur_t,iter,ag_r,ab_r,rb_r,best_e)->bool:
        if(best_e !=-162 and cur_t<=final_t):
            print("solver fail.")
        return int(best_e) == -162 or cur_t <= final_t
