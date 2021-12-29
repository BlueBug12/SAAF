import _sa
import sys
import custom.TSP as m
from custom.TSP import parser
from custom.nodes_generator import NodeGenerator

def main():
    descent_rate = 0.995
    initial_t = 1000
    final_t = 1e-8
    scale = 0.5
    markov_iter = 1
    scale_descent_rate = 0
    #c = m.CustomClass(parser(sys.argv[1]))
    c = m.CustomClass(NodeGenerator(200,200,70).generate())
    c.trivialInitial()
    #c.greedyInitial()
    sa = _sa.SA(c)
    sa.setParam(descent_rate,initial_t,final_t,scale,markov_iter,scale_descent_rate)
    sa.run(True,100)
    sa.showReport()
    c.animate("animation.gif")
    c.visual()

if __name__ == "__main__":
    main()

