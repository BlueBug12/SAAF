#include "_sa.hpp"
namespace py = pybind11;

double SA::acceptance(double old_e, double new_e, double temperature ){
    return std::exp((old_e - new_e)/temperature); 
}

void SA::setParam(double descent_rate, double initial_t, double final_t, double scale, size_t markov_iter, int n_var, double scale_descent_rate){
    m_descent_rate = descent_rate;
    m_initial_t = initial_t;
    m_final_t = final_t;
    m_scale = scale;
    m_markov_iter = markov_iter;
    m_n_var = n_var;
    m_scale_descent_rate = scale_descent_rate;
}

void SA::setInitialState(std::vector<double>initial){
    m_initial_state = initial;
}

void SA::run(){
    double cur_t = m_initial_t;    
    std::vector<double>cur_state = m_initial_state;
    std::vector<double>sol; 
    double cur_e = getEnergy(cur_state);
    double best_e  = cur_e;

    int accept_good = 0;
    int accept_bad = 0;
    int reject_bad = 0;
    std::random_device rd;
    std::default_random_engine eng(rd());
    std::uniform_real_distribution<double> distr(0, 1);

    while(cur_t >= m_final_t){
        for(size_t k = 0;k<m_markov_iter;++k){
            std::vector<double>new_state = neighbor(cur_state);
            double new_e = getEnergy(new_state);
            if(new_e < cur_e){//better state than the current one
                cur_e = new_e;
                cur_state.clear();
                cur_state = new_state;
                accept_good+=1;
            }else{
                double prob = acceptance(cur_e,new_e,cur_t);
                if(prob > distr(eng)){
                    cur_e = new_e;
                    cur_state.clear();
                    cur_state = new_state;
                    accept_bad+=1;
                }else{
                    reject_bad+=1;
                }
            }
            if(best_e > cur_e){
                best_e = cur_e;
                sol = cur_state;
                m_scale*=m_scale_descent_rate;
            }
        }
        cur_t *= m_descent_rate;
    }
    std::cout<<"accept good:"<<accept_good<<std::endl;
    std::cout<<"accept bad:"<<accept_bad<<std::endl;
    std::cout<<"reject bad:"<<reject_bad<<std::endl;
    std::cout<<"result: "<<sol[0]<<","<<sol[1]<<std::endl;
}


double SA::getEnergy(std::vector<double>state){
    double sum = 0.f;
    for(int i=0;i<m_n_var;++i){
        sum += state[i]*std::sin(std::sqrt(std::abs(state[i])));
    }
    return 418.9829*m_n_var - sum;    
}

std::vector<double> SA::neighbor(std::vector<double>state){
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<double> dis(0.0,1.0);
    std::vector<double> next_state = state;
    int i = std::rand()%m_n_var;
    double n = state[i] + m_scale*1000*dis(gen);
    n = std::min(n,500.0);
    next_state[i] = std::max(n,-500.0);
    return next_state;
}


PYBIND11_MODULE(_sa, m){
    m.doc() = "SAAF";
    py::class_<SA>(m,"SA")
        .def(py::init<>())
        .def("setInitialState",&SA::setInitialState)
        .def("setParam",&SA::setParam)
        .def("acceptance",&SA::acceptance)
        .def("run",&SA::run)
        .def("getEnergy",&SA::getEnergy);
}
