#include <iostream>
#include <vector>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
class SA{
   public:
       SA() = default;
       SA(SA const &) = delete;
       SA(SA &&) = delete;
       SA & operator=(SA const &) = delete;
       SA & operator=(SA &&) = delete;
       ~SA();

       void setParam(float descent_rate, float initial_t, float final_t, float scale, size_t markov_iter, int n_var, float scale_descent_rate);
       void setInitialSate();
       bool acceptance(float old_e, float new_e, float temperature);
       void run();
       float getEnergy(std::vector<float>state);
       std::vector<float> neighbor(std::vector<float>state);

   private:
       float m_descent_rate;
       float m_initial_t;
       float m_final_t;
       float m_scale;
       float m_energy;
       size_t m_markov_iter;
       int   m_n_var;
       float m_scale_descent_rate;
       std::vector<float> m_initial_state;

       
};
