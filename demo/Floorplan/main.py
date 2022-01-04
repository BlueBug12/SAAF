import _sa
import sys
import custom.Floorplan as m

def main():
    descen_rate = 0.7
    initial_t = 1000.0
    final_t = 1.0
    scale = 0.5
    markov_iter = 10000
    scale_descent_rate = 0
    alpha = float(sys.argv[1])
    block_file = sys.argv[2]
    nets_file = sys.argv[3]
    output_file = sys.argv[4]
    c = m.CustomClass(block_file,nets_file,alpha,output_file)
    sa = _sa.SA(c)
    sa.setParam(descen_rate,initial_t,final_t,scale,markov_iter,scale_descent_rate)
    sa.run(True,1)
    c.visual("result.png")
    c.animation("result.gif")
    sa.showReport()
    sa.output()
    sa.writeHistory("output.csv")
    sa.plot()

if __name__ == "__main__":
    main()
