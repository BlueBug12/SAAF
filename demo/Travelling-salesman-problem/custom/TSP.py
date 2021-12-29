import _sa
import random
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def parser(filename):
    coords=[]
    with open(filename) as f:
        n = int(f.readline().split()[0])
        for i in range(n):
            coord = f.readline().split()
            coords.append([float(pos) for pos in coord])
    return coords

def plotTSP(paths, points, num_iters=1):

    x = []; y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])

    plt.plot(x, y, 'co')

    # Set a scale for the arrow heads (there should be a reasonable default for this, WTF?)
    a_scale = float(max(x))/float(100)

    # Draw the older paths, if provided
    if num_iters > 1:

        for i in range(1, num_iters):

            # Transform the old paths into a list of coordinates
            xi = []; yi = [];
            for j in paths[i]:
                xi.append(points[j][0])
                yi.append(points[j][1])

            plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]),
                    head_width = a_scale, color = 'r',
                    length_includes_head = True, ls = 'dashed',
                    width = 0.001/float(num_iters))
            for i in range(0, len(x) - 1):
                plt.arrow(xi[i], yi[i], (xi[i+1] - xi[i]), (yi[i+1] - yi[i]),
                        head_width = a_scale, color = 'r', length_includes_head = True,
                        ls = 'dashed', width = 0.001/float(num_iters))

    # Draw the primary path for the TSP problem
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = a_scale,
            color ='g', length_includes_head=True)
    for i in range(0,len(x)-1):
        plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale,
                color = 'g', length_includes_head = True)

    #Set axis too slitghtly larger than the set of x and y
    plt.xlim(min(x)*1.1, max(x)*1.1)
    plt.ylim(min(y)*1.1, max(y)*1.1)
    plt.show()

def animateTSP(history, points, filename):
    points = np.array(points)
    key_frames_mult = len(history) // 100

    fig, ax = plt.subplots()

    line, = plt.plot([], [], lw=2)

    def init():
        ''' initialize node dots on graph '''
        x = [points[i][0] for i in history[0]]
        y = [points[i][1] for i in history[0]]
        plt.plot(x, y, 'co')

        ''' draw axes slighty bigger  '''
        extra_x = (max(x) - min(x)) * 0.05
        extra_y = (max(y) - min(y)) * 0.05
        ax.set_xlim(min(x) - extra_x, max(x) + extra_x)
        ax.set_ylim(min(y) - extra_y, max(y) + extra_y)

        '''initialize solution to be empty '''
        line.set_data([], [])
        return line,

    def update(frame):
        ''' for every frame update the solution on the graph '''
        x = [points[i, 0] for i in history[frame] + [history[frame][0]]]
        y = [points[i, 1] for i in history[frame] + [history[frame][0]]]
        line.set_data(x, y)
        return line

    ''' animate precalulated solutions '''

    ani = FuncAnimation(fig, update, frames=range(0, len(history), key_frames_mult),
                        init_func=init, interval=3, repeat=False)
    ani.save(filename, writer='pillow', fps=30)
    plt.show()

class CustomClass():
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords)
        self.state = []
        self.segment=[0,0]
        self.best_state = []
        self.history = []
   
    def trivialInitial(self):
        self.state = [i for i in range(self.n)]
        self.history = [self.state]

    def greedyInitial(self):
        cur_node = random.randint(0,self.n-1)
        self.state = [cur_node]
        free_nodes = set([i for i in range(self.n)])
        free_nodes.remove(cur_node)
        while free_nodes:
            next_node = min(free_nodes,key=lambda x:self.dist(cur_node,x))
            free_nodes.remove(next_node)
            self.state.append(next_node)
            cur_node = next_node
        self.history = [self.state]

    def dist(self,n1,n2):
        c1 = self.coords[n1]
        c2 = self.coords[n2]
        return math.sqrt((c1[0]-c2[0])**2+(c1[1]-c2[1])**2)

    def visual(self,state = None):
        if state == None:
            state = self.best_state
        plotTSP([state],self.coords)
    
    def animate(self,filename):
        animateTSP(self.history,self.coords,filename)

    def jumpState(self,scale,cur_t, iter):
        self.segment = random.sample(self.state,2)
        self.reverse()
        self.history.append(list(np.copy(self.best_state)))
        #self.history.append(list(np.copy(self.state)))

    def reverse(self):
        self.state[self.segment[0]:self.segment[1]] = reversed(self.state[self.segment[0]:self.segment[1]])

    def storeBest(self):
        self.best_state = np.copy(self.state)

    def getEnergy(self, best =False)->float:
        cost = 0
        state = []
        if best:
            state = self.best_state
        else:
            state = self.state
        for i in range(self.n):
            cost += self.dist(state[i%self.n],state[(i+1)%self.n])
        return cost

    def output(self):
        pass
        
    def stopCondition(self,final_t,energy,cur_t,iter,ag_r,ab_r,rb_r,best_e)->bool:
        return cur_t < final_t

