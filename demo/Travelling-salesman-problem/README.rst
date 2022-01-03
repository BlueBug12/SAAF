===============================================
SAAF Demonstration: Travelling-salesman problem
===============================================

Description
===========
The **travelling-salesman problem** is a classic **NP-complete** problem in graph theory, it asks the following question: "Given a list of cities and the distances 
between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?". It is also a good example 
to visualize the process of simulated annealing, so I made some functions to generate the picture of final result and animation to show each state of the process. 

Execution
=========

::

  make  
  python3 main.py [testbench]

If you don't have the testbench, you can ignore the input parameter and let `NodeGenerator` generates the data automatically

or just use the default setting::

  make run


Reference
=========
[1] `TSP animation 
<https://github.com/jedrazb/python-tsp-simulated-annealing>`__

[2] `TSP graph
<https://github.com/chncyhn/simulated-annealing-tsp>`__

[3] `Testbench generator
<https://www.mathopenref.com/coordpolycalc.html>`__

