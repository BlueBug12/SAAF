import _sa
import pytest
import numpy as np
import math
import random

sa = _sa.SA()
sa.setParam(0.98,100.0,1.0,0.5,100,2,0.99)

def acceptance(delta_energy: float, temperature: float):
	return math.exp(-delta_energy/temperature)

def getEnergy(state,n_var):
	sum_ = 0.0
	for i in range(n_var):
		sum_ += state[i]*np.sin(np.sqrt(abs(state[i])))
	return 418.9829*n_var - sum_

def test_aaceptance():
    n1_n = 54.43
    n1_o = 45.3
    n2_n = -4.66
    n2_o = 5.462
    n3_n = -435.46
    n3_o = 93.3

    assert(sa.acceptance(n1_o,n1_n,54.1)==acceptance(n1_n-n1_o,54.1))
    assert(sa.acceptance(n2_o,n2_n,64.54)==acceptance(n2_n-n2_o,64.54))
    assert(sa.acceptance(n3_o,n3_n,4.2)==acceptance(n3_n-n3_o,4.2))



def test_energy():
	x1 = np.zeros(2)
	x2 = np.zeros(2)
	x3 = np.zeros(2)
	for v in range(2):
		x1[v] = random.uniform(-500,500)
		x2[v] = random.uniform(-500,500)
		x3[v] = random.uniform(-500,500)
		
	assert(getEnergy(x1,2)==sa.getEnergy(x1))
	assert(getEnergy(x2,2)==sa.getEnergy(x2))
	assert(getEnergy(x3,2)==sa.getEnergy(x3))
    
