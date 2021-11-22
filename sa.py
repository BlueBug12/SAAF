import _sa
#import pytest
import random
import numpy as np

sa = _sa.SA();
sa.setParam(0.98,100.0,1.0,0.5,100,2,0.99);
'''
sa.setParam(
        descent_rate = 0.98,
        initial_t = 100.0,
        final_t = 1.0,
        scale = 0.5,
        markov_iter = 100,
        n_var = 2,
        scale_descent_rate = 0.99);
'''
x_min = [-500,-500]
x_max = [500,500]
initial = np.zeros(2)
for v in range(2):
    initial[v] = random.uniform(x_min[v],x_max[v])

sa.setInitialState(initial)

sa.run();

