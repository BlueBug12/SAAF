#include "_sa.hpp"

SA::SA(py::object py_class){
    libpy = py_class;
}

double SA::acceptance(double old_e, double new_e, double temperature ){
    return std::exp((old_e - new_e)/temperature); 
}

void SA::setParam(double descent_rate, double initial_t, double final_t, double scale, int markov_iter, double scale_descent_rate){
    m_descent_rate = descent_rate;
    m_initial_t = initial_t;
    m_final_t = final_t;
    m_scale = scale;
    m_markov_iter = markov_iter;
    m_scale_descent_rate = scale_descent_rate;
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
    double e_sum = 0.0;
    size_t iter = 0;
    double accept_good_rate = 0.0;
    double accept_bad_rate = 0.0;
    double reject_bad_rate = 0.0;

    std::random_device rd;
    std::default_random_engine eng(rd());
    std::uniform_real_distribution<double> distr(0, 1);

    while(stopCondition(cur_t, iter,accept_good_rate,accept_bad_rate,reject_bad_rate)){
        clock_t start = clock();
        for(int k = 0;k<m_markov_iter;++k){
            jumpState(m_scale,cur_t,iter);
            double new_e = getEnergy();
            e_sum += new_e;
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
        clock_t end = clock();
        record r(iter,e_sum/(double)m_markov_iter,cur_t,best_e,accept_good_rate,accept_bad_rate,reject_bad_rate,(end-start)/CLOCKS_PER_SEC);
        records.push_back(std::move(r));
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
        e_sum = 0.0;
    }
    std::cout<<"accept good:"<<accept_good<<std::endl;
    std::cout<<"accept bad:"<<accept_bad<<std::endl;
    std::cout<<"reject bad:"<<reject_bad<<std::endl;
    output();
}

double SA::getEnergy(){
    return libpy.attr("getCost")().cast<double>();
}

void SA::reverse(){
    libpy.attr("reverse")();    
}

void SA::jumpState(double scale, double cur_t, int iter){
    libpy.attr("jumpState")(scale,cur_t,iter);
}

void SA::storeBest(){
    libpy.attr("storeBest")();
}

void SA::output(){
    libpy.attr("output")();
}

bool SA::stopCondition(double cur_t,int iter, double ag_r, double ab_r, double rb_r){
    return libpy.attr("stopCondition")(m_final_t,m_energy,cur_t,iter,ag_r,ab_r,rb_r).cast<bool>();
}

void SA::writeHistory(std::string file_name){
    std::ofstream fout{file_name};
    fout <<"iteration,average energy,temperature,lowest energy,accept good rate,accept bad rate,reject rate,time period" << std::endl;
    for(size_t i=0;i<records.size();++i){
        record & r = records.at(i);
        fout << r.iteration << "," << r.energy << "," << r.temperature << "," 
            << r.best_energy << "," << r.good_accept_rate << "," 
            << r.bad_accept_rate << "," << r.reject_rate << "," 
            << r.period << std::endl;
    }
    fout.close();
}

PYBIND11_MODULE(_sa, m){
    m.doc() = "SAAF";
    py::class_<SA>(m,"SA")
        .def(py::init<py::object>())
        .def("getEnergy",&SA::getEnergy)
        .def("setParam",&SA::setParam)
        .def("acceptance",&SA::acceptance)
        .def("run",&SA::run)
        .def("writeHistory",&SA::writeHistory);
}
