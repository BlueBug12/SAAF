#include "_sa.hpp"


bool SA::acceptance(float old_e, float new_e, float temperature ){
    return std::exp((old_e - new_e)/temperature); 
}

void SA::setParam(float descent_rate, float initial_t, float final_t, float scale, size_t markov_iter, int n_var, float sale_descent_rate){
    m_descent_rate = descent_rate;
    m_initial_t = initial_t;
    m_final_t = final_t;
    m_scale = scale;
    m_markov_iter = markov_iter;
    m_n_var = n_var;
    m_scale_descent_rate = scale_descent_rate;
}

void SA::run(){
    float cur_t = m_initial_t;    
    std::vector<float>cur_state = m_initial_state;
    
    float cur_e = getEnergy(cur_state);
    float best_e  = cur_e;

    while(cur_t >= m_final_t){
        for(size_t k = 0;k<m_markov_iter;++k){
            std::vector<float>new_state = neighbor(cur_state);
            float new_e = getEnergy(new_state);
            if(new_e < cur_e){//better state than the current one
                cur_e = new_e;
                cur_state.clear();
                cur_state = new_state;
                m_scale*=m_scale_descent_rate;
            }else{
                if(acceptance(cur_e,new_e,cur_t)){
                    cur_e = new_e;
                    cur_state.clear();
                    cure_state = new_state;

                }else{
                    //
                }
            }
            if(best_e > cur_e){
                best_e = cur_e;
            }
        }
        cur_t *= m_descent_rate;
    }
}


float SA::getEnergy(std::vector<float>state){
    return 0.0;    
}

std::vector<float> SA::neighbor(std::vector<float>state){
    return state;
}

PYBIND11_MODULE(_sa, m){
    m.doc() = "SAAF";
    pybind11::class_<SA>(m,"SA")
        .def(pybind11::init<>())
        .def("setParam",&SA::setParam)
        .def("acceptance",&SA::acceptance)
        .def("run",&SA::run)
}
