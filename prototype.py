import _sa
import random
import numpy as np
import sys


class CustomClass():
    def __init__(self):
        pass
    
    def jumpState(self,scale,cur_t, iter):
        pass

    def reverse(self):
        pass

    def storeBest(self):
        pass

    def getEnergy(self)->float:
        pass

    def output(self):
        pass
        
    def stopCondition(self,final_t,energy,cur_t,iter,ag_r,ab_r,rb_r)->bool:
        pass 

def main():
    #parameter setting--------------------------
    descen_rate = 0.7
    initial_t = 1000.0
    final_t = 1.0
    scale = 0.5
    markov_iter = 10000
    scale_descent_rate = 0
    show = True
    logger_iter = 1
    history_file = "output.csv"
    #-------------------------------------------


    #custom part--------------------------------
    #---------write what you need here----------
    #-------------------------------------------


    #demonstrate how to use SAAF----------------
    sa = _sa.SA(CustomClss())
    sa.setParam(descen_rate,initial_t,final_t,scale,markov_iter,scale_descent_rate)
    sa.run(show,logger_iter)
    sa.showReport()
    sa.output()
    sa.writeHistory(history_file)
    sa.plot()
    #-------------------------------------------

if __name__ == "__main__":
    main()
