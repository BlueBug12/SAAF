================================================
SAAF : a Simulated-Annealing Algorithm Framework
================================================

API
===
These functions are actually written with C++ and wrapped by `pybind11`, they are the basic architecture of SA process. User should set the parameter properly, and call the functions if needed.
.. code-block:: python
    
    def setParam()

.. code-block:: python

   def run(show, logger_iter)
Define whether to display the logger, and the period of iteration to show it.

.. code-block:: python
    
    def showReport()
Show the SA report.

.. code-block:: python

    def writeHistory(filename)
Write the data into CSV file. 

.. code-block:: python

    def plot()
 Plot the temperature history.


User defined function
=====================
These functions are wrapped into the customized class, and will be called by the C++ SA kernel. In other words, user should define the problem they want to solve in these functions,
so that SAAF can run correctly to get the solution.

.. code-block:: python

    def jumpState(self,scale,cur_t, iter)
Define how to jump to next state according the current temperature `cur_t`, scaling ratio `scale` and iteration `iter`.

.. code-block:: python

    def reverse(self)
Define how to go to the previous state if the current state is rejected.

.. code-block:: python

    def storeBest(self)
Store the currently best solution.

.. code-block:: python
    
    def getEnergy(self)->float
Define the energy of the current state. Notice that the state should be store in the attribute of the customized class(by `jumpState()`), so this function can compute its energy.

.. code-block:: python
    
    def output(self)
This function will be called when the SA process end. User can print some information or write files to record the result.

.. code-block:: python
    
    def stopCondition(self,final_t,energy,cur_t,iter,ag_r,ab_r,rb_r)->bool
Define in what condition should the SA process be stopped.
    - `final_t`: final temperature
    - `energy`: current energy
    - `cur_t`: current temperature
    - `iter`: current iteration
    - `ag_r`: rate of accepting good solution(in current temperature)
    - `ab_r`: rate of accepting bad solution
    - `rb_r`: rate of rejecting bad solution



    





    
