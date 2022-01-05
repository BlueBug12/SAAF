import _sa
import sys
import custom.Sudoku as m

def main():
    descent_rate = 0.99999
    initial_t = 0.5
    final_t = 0
    scale = 0.5
    markov_iter = 1
    scale_descent_rate = 0
    filename = sys.argv[1]
    c = m.CustomClass(filename)
    print("Initial sudoku:")
    c.view()
    c.random_fill()
    sa = _sa.SA(c)
    sa.setParam(descent_rate,initial_t,final_t,scale,markov_iter,scale_descent_rate)
    sa.run(True,1000)
    sa.plot("energy.png")
    print("\nSolved sudoku:")
    c.view()

if __name__ == "__main__":
    main()
