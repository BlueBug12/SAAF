#import _sa
import random
import numpy as np
import sys

outline_width = 0
outline_height = 0
block_num = 0
terminal_num = 0
nets_num = 0
width = []
height = []
pos_x = []
pos_y = []
nets = []
index_map = {}


def parser(block_file,nets_file):
    with open(block_file,'r') as fin:
        #outline width height
        line = fin.readline()
        words = line.split()
        outline_width = int(words[1])
        outline_height = int(words[2])

        #numblock num
        line = fin.readline()
        words = line.split()
        block_num = int(words[1])

        #numterminal num
        line = fin.readline()
        words = line.split()
        terminal_num = int(words[1])

        fin.readline()
        while len(width)!=block_num:
            line = fin.readline()
            while len(line)<=1:
                line = fin.readline()
            words = line.split()
            index_map[words[0]] = len(width)
            width.append(int(words[1]))
            height.append(int(words[2]))
            pos_x.append(0)
            pos_y.append(0)
        
        pin_num = block_num + terminal_num
        while len(pos_x) != pin_num:
            line = fin.readline()
            while len(line)<=1:
                line = fin.readline()
            words = line.split()
            index_map[words[0]] = len(pos_x)
            pos_x.append(int(words[2]))
            pos_y.append(int(words[3]))

    with open(nets_file,'r') as fin:
        line = fin.readline()
        words = line.split()
        nets_num = int(words[1])

        for i in range(nets_num):
            line = fin.readline()
            words = line.split()
            degree = int(words[1])
            nets.append([])
            for j in range(degree):
                pin_name = fin.readline().replace('\n','')
                pin_index = index_map[pin_name]
                nets[-1].append(pin_index)




                





#sa = _sa.SA()
#sa.setParam(0.7,1000.0,1.0,1.0,100000,block_num*2,1.0)
def main():
    alpha = float(sys.argv[1])
    block_file = sys.argv[2]
    nets_file = sys.argv[3]

    parser(block_file,nets_file)

if __name__ == "__main__":
    main()
