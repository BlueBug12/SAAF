#include "_sa.hpp"
#include <tuple>

#define TYPE2 std::pair<int,double>
namespace py = pybind11;
double SA::acceptance(double old_e, double new_e, double temperature ){
    return std::exp((old_e - new_e)/temperature); 
}

void SA::setParam(double descent_rate, double initial_t, double final_t, double scale, int markov_iter, int n_var, double scale_descent_rate){
    m_descent_rate = descent_rate;
    m_initial_t = initial_t;
    m_final_t = final_t;
    m_scale = scale;
    m_markov_iter = markov_iter;
    m_n_var = n_var;
    m_scale_descent_rate = scale_descent_rate;
    py::object Floorplan = py::module_::import("floorplan").attr("Floorplan");
    libpy = Floorplan();
}


void SA::run(){
    
    double cur_t = m_initial_t;    
    double cur_e = getEnergy();
    double best_e  = cur_e;

    int accept_good = 0;
    int accept_bad = 0;
    int reject_bad = 0;
    int local_ag = 0;
    int local_ab = 0;
    int local_rb = 0;
    size_t iter = 0;
    double accept_good_rate = 0.0;
    double accept_bad_rate = 0.0;
    double reject_bad_rate = 0.0;

    std::random_device rd;
    std::default_random_engine eng(rd());
    std::uniform_real_distribution<double> distr(0, 1);

    while(reject_bad_rate <= 0.95 && cur_t > m_final_t){
        for(int k = 0;k<m_markov_iter;++k){
            neighbor();
            double new_e = getEnergy();
            if(new_e < cur_e){//better state than the current one
                cur_e = new_e;
                local_ag += 1;
            }else{
                double prob = acceptance(cur_e,new_e,cur_t);
                if(prob > distr(eng)){
                    cur_e = new_e;
                    local_ab += 1;
                }else{
                    reverse();
                    local_rb += 1;
                }
            }
            if(best_e > cur_e){
                storeBest();
                best_e = cur_e;
                m_scale*=m_scale_descent_rate;
            }
        }
        //record r(iter,cur_e,cur_t,best_e,local_ag/m_markov_iter,local_ab/m_markov_iter,local_rb/m_markov_iter);
        //records.push_back(std::move(r));
        int den = local_ag + local_ab + local_rb;
        accept_good_rate = (double)local_ag/den;
        accept_bad_rate = (double)local_ab/den;
        reject_bad_rate = (double)local_rb/den;
        std::cout<<"iteration "<<iter<<std::endl;
        std::cout<<"accept good rate:"<<accept_good_rate<<std::endl;
        std::cout<<"accept bad rate:"<<accept_bad_rate<<std::endl;
        std::cout<<"reject bad rate:"<<reject_bad_rate<<std::endl;
        std::cout<<"cost:"<<best_e<<std::endl<<std::endl;

        cur_t *= m_descent_rate;
        ++iter;
        accept_good += local_ag;
        accept_bad += local_ab;
        reject_bad += local_rb;
        local_ag = local_ab = local_rb = 0;
    }
    std::cout<<"accept good:"<<accept_good<<std::endl;
    std::cout<<"accept bad:"<<accept_bad<<std::endl;
    std::cout<<"reject bad:"<<reject_bad<<std::endl;
    output();
}

double SA::getEnergy(){
    double dummy = 0.0;
    py::object d = py::cast(dummy);
    d = libpy.attr("getCost")();
    return d.cast<double>();
}

void SA::reverse(){
    libpy.attr("reverse")();    
}

void SA::neighbor(){
    libpy.attr("neighbor")();
}

void SA::storeBest(){
    libpy.attr("storeBest")();
}

void SA::output(){
    libpy.attr("output")();
}
//#define TYPE double

PYBIND11_MODULE(_sa, m){
    m.doc() = "SAAF";
    py::class_<SA>(m,"SA")
        .def(py::init<>())
        .def("getEnergy",&SA::getEnergy)
        .def("setParam",&SA::setParam)
        .def("acceptance",&SA::acceptance)
        .def("run",&SA::run);
}
