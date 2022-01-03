import _sa
import sys
import custom.TSP as m
from custom.TSP import parser
import numpy as np

descent_rate = 0.995
initial_t = 1000
final_t = 1e-8
scale = 0.5
markov_iter = 100
scale_descent_rate = 0
c = m.CustomClass(parser("testbench/100-sided.txt"))
c.trivialInitial()
#c.greedyInitial()
sa = _sa.SA(c)
sa.setParam(descent_rate,initial_t,final_t,scale,markov_iter,scale_descent_rate)
sa.run(True,100)
final_e = c.getEnergy(best=True)

def test_improvement():
    assert(np.isclose(final_e,2*np.pi*100,rtol=1e-02,atol=1e-01))
