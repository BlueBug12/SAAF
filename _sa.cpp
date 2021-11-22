#include "_sa.hpp"
namespace py = pybind11;

bool SA::acceptance(float old_e, float new_e, float temperature ){
    return std::exp((old_e - new_e)/temperature); 
}

void SA::setParam(float descent_rate, float initial_t, float final_t, float scale, size_t markov_iter, int n_var, float scale_descent_rate){
    m_descent_rate = descent_rate;
    m_initial_t = initial_t;
    m_final_t = final_t;
    m_scale = scale;
    m_markov_iter = markov_iter;
    m_n_var = n_var;
    m_scale_descent_rate = scale_descent_rate;
}

void SA::setInitialState(std::vector<float>initial){
    m_initial_state = initial;
}

void SA::run(){
    float cur_t = m_initial_t;    
    std::vector<float>cur_state = m_initial_state;
    std::vector<float>sol; 
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
            }else{
                if(acceptance(cur_e,new_e,cur_t)){
                    cur_e = new_e;
                    cur_state.clear();
                    cur_state = new_state;

                }else{
                    //
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
    std::cout<<"result: "<<sol[0]<<","<<sol[1]<<std::endl;
}


float SA::getEnergy(std::vector<float>state){
    float sum = 0.f;
    for(size_t i=0;i<m_n_var;++i){
        sum += state[i]*std::sin(std::abs(state[i]));
    }
    return sum;    
}

std::vector<float> SA::neighbor(std::vector<float>state){
    std::default_random_engine generator;
    std::normal_distribution<float> distribution(1.0,0.0);
    std::vector<float> next_state = state;
    int i = std::rand()%m_n_var;
    float n = state[i] + m_scale*1000*distribution(generator);
    n = std::min(n,(float)500.0);
    next_state[i] = std::max(n,(float)-500.0);
    return next_state;
}

void test(){
    std::cout<<"test"<<std::endl;
}

PYBIND11_MODULE(_sa, m){
    m.doc() = "SAAF";
    m.def("test",&test);
    py::class_<SA>(m,"SA")
        .def(py::init<>())
        .def("setInitialState",&SA::setInitialState)
        .def("setParam",&SA::setParam)
        .def("acceptance",&SA::acceptance)
        .def("run",&SA::run);
}
