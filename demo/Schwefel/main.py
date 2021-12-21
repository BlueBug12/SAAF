import _sa
import random
import numpy as np
import sys
import custom.Schwefel as m

def main():
    #parameter setting-----
    descen_rate = 0.98
    initial_t = 100.0
    final_t = 1.0
    scale = 0.5
    markov_iter = 100
    scale_descent_rate = 0.99
    show = True
    logger_iter = 10
    history_file = "output.csv"
    #---------------------

    #custom part----------
    n_var = 10 
    x_min = np.full(n_var,-500)
    x_max = np.full(n_var,500)
    #--------------------

    sa = _sa.SA(m.CustomClass(n_var,x_min,x_max))
    sa.setParam(descen_rate,initial_t,final_t,scale,markov_iter,scale_descent_rate)
    sa.run(show,logger_iter)
    sa.showReport()
    sa.output()
    sa.writeHistory(history_file)
    sa.plot()

if __name__ == "__main__":
    main()
