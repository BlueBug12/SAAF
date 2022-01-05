import _sa
import sys
import numpy as np
import pytest
import custom.Sudoku as m

descent_rate = 0.99999
initial_t = 0.5
final_t = 0
scale = 0.5
markov_iter = 100
scale_descent_rate = 0
filename = sys.argv[-1]
c = m.CustomClass(filename)
original = c.getResult()

c.random_fill()
sa = _sa.SA(c)
sa.setParam(descent_rate,initial_t,final_t,scale,markov_iter,scale_descent_rate)
sa.run(True,1000)

result = c.getResult()


def test_same_sudoku():
    non_zero_pos = np.array([i for i in range(81) if original[i] != 0])
    assert(np.alltrue(original[non_zero_pos]==result[non_zero_pos]))

rule = [1,2,3,4,5,6,7,8,9]
def test_blocks():
    for b in range(9):
        row_base = (b//3)*3
        col_base = (b%3)*3
        indices = np.array([col_base + (i%3) + 9*(row_base+(i//3)) for i in range(9)])
        numbers = result[indices]
        assert(rule==sorted(numbers))

def test_rows():
    for r in range(9):
        indices = np.array([i + 9*r for i in range(9)])
        numbers = result[indices]
        assert(rule==sorted(numbers))

def test_cols():
    for c in range(9):
        indices = np.array([c + 9*i for i in range(9)])
        numbers = result[indices]
        assert(rule==sorted(numbers))

