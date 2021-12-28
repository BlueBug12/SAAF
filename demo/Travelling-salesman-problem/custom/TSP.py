import _sa
import random
import numpy as np
import sys
import math

def parser(filename):
    coords=[]
    with open(filename) as f:
        n = int(f.readline().split()[0])
        for i in range(n):
            coord = f.readline().split()
            coords.append([float(pos) for pos in coord])
    return coords

class CustomClass():
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords)
        self.state = []
        self.segment=[0,0]
        self.best_state = []
        self.setInital()
    
    def setInital(self):
        cur_node = random.randint(0,self.n-1)
        self.state = [cur_node]
        free_nodes = set([i for i in range(self.n)])
        free_nodes.remove(cur_node)
        while free_nodes:
            next_node = min(free_nodes,key=lambda x:self.dist(cur_node,x))
            free_nodes.remove(next_node)
            self.state.append(next_node)
            cur_node = next_node

    def dist(self,n1,n2):
        c1 = self.coords[n1]
        c2 = self.coords[n2]
        return math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)

    def jumpState(self,scale,cur_t, iter):
        self.segment = random.sample(self.state,2)
        self.reverse()

    def reverse(self):
        self.state[self.segment[0]:self.segment[1]] = reversed(self.state[self.segment[0]:self.segment[1]])

    def storeBest(self):
        self.best_state = np.copy(self.state)

    def getEnergy(self)->float:
        cost = 0
        for i in range(self.n):
            cost += self.dist(self.state[i%self.n],self.state[(i+1)%self.n])
        return cost

    def output(self):
        pass
        
    def stopCondition(self,final_t,energy,cur_t,iter,ag_r,ab_r,rb_r,best_e)->bool:
        return cur_t < final_t

