#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

struct record{
    record(int iter, double e, double t, double best_e, double g_rate, double b_rate, double r_rate):
        iteration(iter),
        energy(e),
        temperature(t),
        best_energy(best_e),
        good_accept_rate(g_rate),
        bad_accept_rate(b_rate),
        reject_rate(r_rate){}
    record() = delete;
    record(record const &) = default;
    record(record &&) = default;
    record & operator=(record const &) = default;
    record & operator=(record &&) = default;
    ~record() = default;

    int iteration;
    double energy;
    double temperature;
    double best_energy;
    double good_accept_rate;
    double bad_accept_rate;
    double reject_rate;
};

class SA{
   public:
       //SA();
       /*
       SA(SA const &) = delete;
       SA(SA &&) = delete;
       SA & operator=(SA const &) = delete;
       SA & operator=(SA &&) = delete;*/
       //~SA();

       void setParam(double descent_rate, double initial_t, double final_t, double scale, size_t markov_iter, int n_var, double scale_descent_rate);
       void setInitialState(std::vector<double>initial);
       double acceptance(double old_e, double new_e, double temperature);
       void run();
       double getEnergy(std::vector<double>state);
       std::vector<double> neighbor(std::vector<double>state);

       std::vector<record>records;

   private:
       double m_descent_rate;
       double m_initial_t;
       double m_final_t;
       double m_scale;
       double m_energy;
       size_t m_markov_iter;
       int   m_n_var;
       double m_scale_descent_rate;
       std::vector<double> m_initial_state;

       
};
