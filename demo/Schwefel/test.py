import _sa
import pytest
import numpy as np
import math
import random
import custom.Schwefel as m

descen_rate = 0.98
initial_t = 100.0
final_t = 1.0
scale = 0.5
markov_iter = 100
scale_descent_rate = 0.99
show = True
logger_iter = 10
#---------------------

#custom part----------
n_var = 10 
x_min = np.full(n_var,-500)
x_max = np.full(n_var,500)
#--------------------

c =m.CustomClass(n_var,x_min,x_max)
sa = _sa.SA(c)
sa.setParam(0.98,100.0,1.0,0.5,100,0.99)
sa.run(show,logger_iter)
print(c.best_state)

def test_result():
    for i in range(n_var):
        assert(np.isclose(c.best_state[i],420.968746,rtol=1e-02,atol=1e-01))

