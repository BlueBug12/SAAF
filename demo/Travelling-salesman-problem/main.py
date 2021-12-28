import _sa
import sys
import custom.TSP as m
from custom.TSP import parser

def main():
    descent_rate = 0.995
    initial_t = 1000
    final_t = 1e-8
    scale = 0.5
    markov_iter = 1
    scale_descent_rate = 0
    c = m.CustomClass(parser(sys.argv[1]))
    sa = _sa.SA(c)
    sa.setParam(descent_rate,initial_t,final_t,scale,markov_iter,scale_descent_rate)
    sa.run(True,100)

if __name__ == "__main__":
    main()

