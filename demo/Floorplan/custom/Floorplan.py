import _sa
import random
import numpy as np
import sys
import copy
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def swapList(list,pos1,pos2):
    x1 = list[pos1]
    x2 = list[pos2]
    list[pos1] = x2
    list[pos2] = x1

class CustomClass():
    def __init__(self, block_file, nets_file, alpha,output_file):
        self.outline_width = 0
        self.outline_height = 0
        self.block_num = 0
        self.terminal_num = 0
        self.nets_num = 0
        self.alpha = alpha
        self.output_file = output_file
        self.option = 0

        self.cur_hpwl = 0
        self.cur_area = 0
        self.cur_width = 0
        self.cur_height = 0
        
        self.best_hpwl = 0
        self.best_area = 0
        self.best_w = 0
        self.best_h = 0
        self.best_width = []
        self.best_height = []
        self.best_pos_x = []
        self.best_pos_y = []

        self.pos_loci = []
        self.neg_loci = []
        self.width = []
        self.height = []
        self.match_x = []
        self.match_y = []
        self.pos_x = []
        self.pos_y = []
        self.nets = []
        self.index_map = {}
        self.op_record = [0,0,0]
        self.bound = []
        self.parser(block_file,nets_file)
        self.setInitial()

    def parser(self,block_file,nets_file):
        with open(block_file,'r') as fin:
            #outline width height
            line = fin.readline()
            words = line.split()
            self.outline_width = int(words[1])
            self.outline_height = int(words[2])

            #numblock num
            line = fin.readline()
            words = line.split()
            self.block_num = int(words[1])

            #numterminal num
            line = fin.readline()
            words = line.split()
            self.terminal_num = int(words[1])

            fin.readline()
            while len(self.width)!=self.block_num:
                line = fin.readline()
                while len(line)<=1:
                    line = fin.readline()
                words = line.split()
                self.index_map[words[0]] = len(self.width)
                self.width.append(int(words[1]))
                self.height.append(int(words[2]))
                self.pos_x.append(0)
                self.pos_y.append(0)
                self.match_x.append(0)
                self.match_y.append(0)
            
            pin_num = self.block_num + self.terminal_num
            while len(self.pos_x) != pin_num:
                line = fin.readline()
                while len(line)<=1:
                    line = fin.readline()
                words = line.split()
                self.index_map[words[0]] = len(self.pos_x)
                self.pos_x.append(int(words[2]))
                self.pos_y.append(int(words[3]))

        with open(nets_file,'r') as fin:
            line = fin.readline()
            words = line.split()
            self.nets_num = int(words[1])

            for i in range(self.nets_num):
                line = fin.readline()
                words = line.split()
                degree = int(words[1])
                self.nets.append([])
                for j in range(degree):
                    pin_name = fin.readline().replace('\n','')
                    pin_index = self.index_map[pin_name]
                    self.nets[-1].append(pin_index)

        self.bound = np.zeros([4,self.nets_num])
    
    def setInitial(self):
        for i in range(self.block_num):
            self.pos_loci.append(i)
            self.neg_loci.append(i)
        random.shuffle(self.pos_loci)
        random.shuffle(self.neg_loci)
        for i in range(self.block_num):
            self.match_x[self.pos_loci[i]] = i
            self.match_y[self.neg_loci[i]] = i

    def updateNet(self):
        self.bound[0].fill(int(1e9))
        self.bound[1].fill(int(-1e9))
        self.bound[2].fill(int(-1e9))
        self.bound[3].fill(int(1e9))
        for i in range(self.nets_num):
            for pin in self.nets[i]:
                self.updateBound(i,pin)

    def updateBound(self,net_id, pos_id):
        assert(net_id<self.nets_num)
        assert(pos_id<self.block_num+self.terminal_num)
        x = self.pos_x[pos_id]
        y = self.pos_y[pos_id]
        if pos_id < self.block_num:
           x += int(self.width[pos_id]/2)
           y += int(self.height[pos_id]/2)
        self.bound[0][net_id] = min(self.bound[0][net_id],x)
        self.bound[1][net_id] = max(self.bound[1][net_id],x)
        self.bound[2][net_id] = max(self.bound[2][net_id],y)
        self.bound[3][net_id] = min(self.bound[3][net_id],y)
    
    def getHPWL(self):
        self.updateNet()
        hpwl = 0
        for i in range(self.nets_num):
            hpwl += (self.bound[1][i]-self.bound[0][i]) + (self.bound[2][i]-self.bound[3][i])
        return hpwl

    def visual(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect('equal',adjustable='box')
        x_lim = self.outline_width
        y_lim = self.outline_height
        for i in range(len(self.width)):
            x_lim = max(self.best_pos_x[i]+self.best_width[i],x_lim)
            y_lim = max(self.best_pos_y[i]+self.best_height[i],y_lim)
            rect = Rectangle((self.best_pos_x[i],self.best_pos_y[i]),self.best_width[i],self.best_height[i], ec = "blue", color = "blue", alpha=0.4)
            ax.add_patch(rect)
        boundary = Rectangle((0,0),self.outline_width,self.outline_height,color="green",alpha=0.2)
        ax.add_patch(boundary)
        plt.xlim([0,x_lim])
        plt.ylim([0,y_lim])
        plt.show()
    
    def jumpState(self,scale,cur_t, iter):
        self.operation(random.randint(1,3))

    def operation(self,op):
        x1 = random.randint(0,self.block_num-1)
        x2 = random.randint(0,self.block_num-1)
        self.option = op
        while x1 == x2:
            x2 = random.randint(0,self.block_num-1)
        if op == 1:
            index = random.randint(0,1)
            if index == 0:
                swapList(self.match_x,self.pos_loci[x1],self.pos_loci[x2])
                swapList(self.pos_loci,x1,x2)
            else:
                swapList(self.match_y,self.neg_loci[x1],self.neg_loci[x2])
                swapList(self.neg_loci,x1,x2)
            self.op_record[0] = x1
            self.op_record[1] = x2
            self.op_record[2] = index
        elif op == 2:
            pos_i1 = self.match_x[x1]
            pos_i2 = self.match_x[x2]
            neg_i1 = self.match_y[x1]
            neg_i2 = self.match_y[x2]
            swapList(self.match_x,x1,x2)
            swapList(self.match_y,x1,x2)
            swapList(self.pos_loci,pos_i1,pos_i2)
            swapList(self.neg_loci,neg_i1,neg_i2)
            self.op_record[0] = x1
            self.op_record[1] = x2
        else:
            self.width[x1],self.height[x1] = self.height[x1], self.width[x1] 
            self.op_record[0] = x1

    
    def reverse(self):
        x1 = self.op_record[0]
        x2 = self.op_record[1]
        if self.option == 1:
            index = self.op_record[2]
            if(index == 0):
                swapList(self.pos_loci,x1,x2)
                swapList(self.match_x,self.pos_loci[x1],self.pos_loci[x2])
            else:
                swapList(self.neg_loci,x1,x2)
                swapList(self.match_y,self.neg_loci[x1],self.neg_loci[x2])
        elif self.option == 2:
            pos_i1 = self.match_x[x1]
            pos_i2 = self.match_x[x2]
            neg_i1 = self.match_y[x1]
            neg_i2 = self.match_y[x2]
            swapList(self.match_x,x1,x2)
            swapList(self.match_y,x1,x2)
            swapList(self.pos_loci,pos_i1,pos_i2)
            swapList(self.neg_loci,neg_i1,neg_i2)
        else:
            self.width[x1],self.height[x1] = self.height[x1], self.width[x1] 


    def storeBest(self):
        self.best_hpwl = self.hpwl
        self.best_area = self.area
        self.best_w = self.cur_width 
        self.best_h = self.cur_height
        self.best_width = copy.deepcopy(self.width)
        self.best_height = copy.deepcopy(self.height)
        self.best_pos_x = copy.deepcopy(self.pos_x)
        self.best_pos_y = copy.deepcopy(self.pos_y)


    def getArea(self):
        lcs = np.zeros(self.block_num)
        for i in range(self.block_num):
            id = self.pos_loci[i]
            p = self.match_y[id]
            self.pos_x[id] = lcs[p]
            t = self.pos_x[id] + self.width[id]
            for j in range(p,self.block_num):
                if t > lcs[j]:
                    lcs[j] = t
                else:
                    break
        w = lcs[-1]
        lcs = np.zeros(self.block_num)
        for i in range(self.block_num):
            id = self.neg_loci[i]
            p = self.block_num - 1 - self.match_x[id]
            self.pos_y[id] = lcs[p]
            t = self.pos_y[id] + self.height[id]
            for j in range(p,self.block_num):
                if t > lcs[j]:
                    lcs[j] = t
                else:
                    break
        h = lcs[-1]
        return w,h

    def skew(self,w,h):
        r = (h*self.outline_width) / (w*self.outline_height)
        if r < 1:
            r = 1/r
        if w > self.outline_width:
            r*=1.1
        if h > self.outline_height:
            r*=1.1
        if w <= self.outline_width and h<= self.outline_height:
            r*=0.8
        return r

    def getEnergy(self):
        self.cur_width, self.cur_height = self.getArea()
        self.area = self.cur_width*self.cur_height
        self.hpwl = self.getHPWL()
        return self.skew(self.cur_width,self.cur_height)*self.alpha*self.area+(1-self.alpha)*self.hpwl

    def output(self):
        with open(self.output_file,"w") as fout:
            fout.write(str(int(self.best_area*self.alpha+(1-self.alpha)*self.best_hpwl))+"\n")
            fout.write(str(int(self.best_hpwl))+"\n")
            fout.write(str(self.best_area)+"\n")
            fout.write(str(int(self.best_w))+" "+str(int(self.best_h))+"\n")
            fout.write("0.87"+"\n")
            inv_map = {v: k for k,v in self.index_map.items()}
            for i in range(self.block_num):
                fout.write(str(inv_map[i])+" "+str(int(self.best_pos_x[i]))+" "+str(int(self.best_pos_y[i]))+" "+str(int(self.best_pos_x[i]+self.best_width[i]))+" "+str(int(self.best_pos_y[i]+self.best_height[i]))+"\n")
        
    def stopCondition(self,final_t,energy,cur_t,iter,ag_r,ab_r,rb_r,best_e):
        return rb_r > 0.95 or cur_t <= final_t
    

