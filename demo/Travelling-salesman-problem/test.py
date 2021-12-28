import _sa
import sys
import custom.TSP as m
from custom.TSP import parser

descent_rate = 0.995
initial_t = 1000
final_t = 1e-8
scale = 0.5
markov_iter = 1
scale_descent_rate = 0
c = m.CustomClass(parser(sys.argv[2]))
c.trivialInitial()
initial_e = c.getEnergy()
#c.greedyInitial()
sa = _sa.SA(c)
sa.setParam(descent_rate,initial_t,final_t,scale,markov_iter,scale_descent_rate)
sa.run(True,100)
final_e = c.getEnergy(best=True)

def test_improvement():
    rate = (initial_e-final_e)/initial_e
    assert(rate>0.1)
    assert(initial_e>final_e)
    assert(final_e > 0)
