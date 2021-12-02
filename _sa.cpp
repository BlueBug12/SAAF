#include "_sa.hpp"
namespace py = pybind11;
template <class T>
double SA<T>::acceptance(double old_e, double new_e, double temperature ){
    return std::exp((old_e - new_e)/temperature); 
}

template <class T>
void SA<T>::setParam(double descent_rate, double initial_t, double final_t, double scale, size_t markov_iter, int n_var, double scale_descent_rate){
    m_descent_rate = descent_rate;
    m_initial_t = initial_t;
    m_final_t = final_t;
    m_scale = scale;
    m_markov_iter = markov_iter;
    m_n_var = n_var;
    m_scale_descent_rate = scale_descent_rate;
}

template <class T>
void SA<T>::setInitialState(std::vector<T>initial){
    m_initial_state = initial;
}

template <class T>
void SA<T>::run(){
    double cur_t = m_initial_t;    
    std::vector<T>cur_state = m_initial_state;
    std::vector<T>sol; 
    double cur_e = getEnergy(cur_state);
    double best_e  = cur_e;

    int accept_good = 0;
    int accept_bad = 0;
    int reject_bad = 0;
    size_t iter = 0;
    std::random_device rd;
    std::default_random_engine eng(rd());
    std::uniform_real_distribution<double> distr(0, 1);

    while(cur_t >= m_final_t){
        int local_a_g = 0;
        int local_a_b = 0;
        int local_r_b = 0;
        for(size_t k = 0;k<m_markov_iter;++k){
            std::vector<T>new_state = neighbor(cur_state);
            double new_e = getEnergy(new_state);
            if(new_e < cur_e){//better state than the current one
                cur_e = new_e;
                cur_state.clear();
                cur_state = new_state;
                local_a_g += 1;
            }else{
                double prob = acceptance(cur_e,new_e,cur_t);
                if(prob > distr(eng)){
                    cur_e = new_e;
                    cur_state.clear();
                    cur_state = new_state;
                    local_a_b += 1;
                }else{
                    local_r_b += 1;
                }
            }
            if(best_e > cur_e){
                best_e = cur_e;
                sol = cur_state;
                m_scale*=m_scale_descent_rate;
            }
        }
        record r(iter,cur_e,cur_t,best_e,local_a_g/m_markov_iter,local_a_b/m_markov_iter,local_r_b/m_markov_iter);
        records.push_back(std::move(r));
        cur_t *= m_descent_rate;
        ++iter;
        accept_good += local_a_g;
        accept_bad += local_a_b;
        reject_bad += local_r_b;
    }
    std::cout<<"accept good:"<<accept_good<<std::endl;
    std::cout<<"accept bad:"<<accept_bad<<std::endl;
    std::cout<<"reject bad:"<<reject_bad<<std::endl;
    std::cout<<"result: "<<sol[0]<<","<<sol[1]<<std::endl;
}


template <class T>
double SA<T>::getEnergy(std::vector<T>state){
    double sum = 0.f;
    for(int i=0;i<m_n_var;++i){
        sum += state[i]*std::sin(std::sqrt(std::abs(state[i])));
    }
    return 418.9829*m_n_var - sum;    
}

template <class T>
std::vector<T> SA<T>::neighbor(std::vector<T>state){
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<double> dis(0.0,1.0);
    std::vector<T> next_state = state;
    int i = std::rand()%m_n_var;
    double n = state[i] + m_scale*1000*dis(gen);
    n = std::min(n,500.0);
    next_state[i] = std::max(n,-500.0);
    return next_state;
}

//#define TYPE double

PYBIND11_MODULE(_sa, m){
    m.doc() = "SAAF";
    py::class_<SA<TYPE>>(m,"SA")
        .def(py::init<>())
        .def("setInitialState",&SA<TYPE>::setInitialState)
        .def("setParam",&SA<TYPE>::setParam)
        .def("acceptance",&SA<TYPE>::acceptance)
        .def("run",&SA<TYPE>::run)
        .def("getEnergy",&SA<TYPE>::getEnergy);
}
