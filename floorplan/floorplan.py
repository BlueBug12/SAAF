import _sa
import random
import numpy as np
import sys

def swapList(list,pos1,pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]

class Floorplan():
    def __init__(self):
        self.outline_width = 0
        self.outline_height = 0
        self.block_num = 0
        self.terminal_num = 0
        self.nets_num = 0
        self.alpha = 0.6
        self.option = 0

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
        self.parser("ami33/ami33.block","ami33/ami33.nets")
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
    
    def setInitial(self):
        for i in range(self.block_num):
            self.pos_loci.append(i)
            self.neg_loci.append(i)
        random.shuffle(self.pos_loci)
        random.shuffle(self.neg_loci)
        for i in range(self.block_num):
            self.match_x[self.pos_loci[i]] = i
            self.match_y[self.neg_loci[i]] = i

    def getHPWL(self):
        return 0
    
    def neighbor(self):
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
            else:
                swapList(self.neg_loci,x1,x2)
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
        return w*h

    def getCost(self):
        return self.alpha*self.getArea()+(1-self.alpha)*self.getHPWL()
    

#sa = _sa.SA()
#sa.setParam(0.7,1000.0,1.0,1.0,100000,block_num*2,1.0)
def main():
    descen_rate = 0.7
    initial_t = 1000.0
    final_t = 1.0
    scale = 0.5
    markov_iter = 10000
    n_var = 2
    scale_descent_rate = 0.3

    sa = _sa.SA()
    sa.setParam(descen_rate,initial_t,final_t,scale,markov_iter,n_var,scale_descent_rate)


    #sa.getEnergy([[0,2,1],[1,0,2]])
    #sa.test([[0,2,1],[1,0,2]])
    sa.run()
    #getCost([[0,1],[1,0]])
    #sa.test()
    '''
    alpha = float(sys.argv[1])
    block_file = sys.argv[2]
    nets_file = sys.argv[3]

    parser(block_file,nets_file)
    print(block_num,"after parser")
    '''

if __name__ == "__main__":
    main()
