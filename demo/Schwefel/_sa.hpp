#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <pybind11/pybind11.h>
#include <pybind11/embed.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace pybind11::literals;

struct record{
    record(int iter, double e, double ave_e, double t, double best_e, double g_rate, double b_rate, double r_rate, double p):
        iteration(iter),
        current_energy(e),
        average_energy(ave_e),
        temperature(t),
        best_energy(best_e),
        good_accept_rate(g_rate),
        bad_accept_rate(b_rate),
        reject_rate(r_rate),
        period(p){}
    record() = delete;
    record(record const &) = default;
    record(record &&) = default;
    record & operator=(record const &) = default;
    record & operator=(record &&) = default;
    ~record() = default;

    int iteration;
    double current_energy;
    double average_energy;
    double temperature;
    double best_energy;
    double good_accept_rate;
    double bad_accept_rate;
    double reject_rate;
    double period;
};

class SA{
   public:
       SA(py::object py_class);
       SA(SA const &) = delete;
       SA(SA &&) = delete;
       SA & operator=(SA const &) = delete;
       SA & operator=(SA &&) = delete;
       ~SA() = default;

       void setParam(double descent_rate, double initial_t, double final_t, double scale, int markov_iter, double scale_descent_rate);
       double acceptance(double old_e, double new_e, double temperature, double gain = 1);
       void run(bool show = true, int logger_iter =  1);
       double getEnergy();
       void reverse();
       void jumpState(double scale, double cur_t, int iter);
       void storeBest();
       void output();
       bool stopCondition(double cur_t, int iter, double ag_r, double ab_r, double rb_r, double best_e);
       void writeHistory(std::string file_name);
       void plot(std::string filename);
       void showReport();
       std::vector<record>records;


       int total_accept_good;
       int total_accept_bad;
       int total_reject_bad;

   private:
       double m_descent_rate;
       double m_initial_t;
       double m_final_t;
       double m_scale;
       double m_energy;
       int m_markov_iter;
       double m_runtime;
       double m_best_e;
       int m_iter;
       double m_scale_descent_rate;
       py::object m_libpy;
};
