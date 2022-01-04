#include "_sa.hpp"

SA::SA(py::object py_class){
    m_iter = 0;
    m_runtime = 0.0;
    total_accept_good = 0;
    total_accept_bad = 0;
    total_reject_bad = 0;
    m_libpy = py_class;
}

double SA::acceptance(double old_e, double new_e, double temperature, double gain){
    return std::exp(((old_e - new_e)*gain)/temperature); 
}

void SA::setParam(double descent_rate, double initial_t, double final_t, double scale, int markov_iter, double scale_descent_rate){
    m_descent_rate = descent_rate;
    m_initial_t = initial_t;
    m_final_t = final_t;
    m_scale = scale;
    m_markov_iter = markov_iter;
    m_scale_descent_rate = scale_descent_rate;
}

void SA::run(bool show, int logger_iter){
    double cur_t = m_initial_t;    
    double cur_e = getEnergy();
    m_best_e  = cur_e;
    clock_t run_beg = clock();
    int local_ag = 0;
    int local_ab = 0;
    int local_rb = 0;
    double e_sum = 0.0;
    double accept_good_rate = 0.0;
    double accept_bad_rate = 0.0;
    double reject_bad_rate = 0.0;

    std::random_device rd;
    std::default_random_engine eng(rd());
    std::uniform_real_distribution<double> distr(0, 1);

    while(!stopCondition(cur_t, m_iter,accept_good_rate,accept_bad_rate,reject_bad_rate,m_best_e)){
        clock_t start = clock();
        for(int k = 0;k<m_markov_iter;++k){
            jumpState(m_scale,cur_t,m_iter);
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
            if(m_best_e > cur_e){
                storeBest();
                m_best_e = cur_e;
                m_scale*=m_scale_descent_rate;
            }
        }
        clock_t end = clock();
        record r(m_iter,cur_e,e_sum/(double)m_markov_iter,cur_t,m_best_e,accept_good_rate,accept_bad_rate,reject_bad_rate,(double)(end-start)/CLOCKS_PER_SEC);
        records.push_back(std::move(r));
        int den = local_ag + local_ab + local_rb;
        accept_good_rate = (double)local_ag/den;
        accept_bad_rate = (double)local_ab/den;
        reject_bad_rate = (double)local_rb/den;
        if(show && m_iter%logger_iter==0){
            std::cout<<"Iteration = "<<std::left<<std::setw(10)<<m_iter;
            std::cout<<"AG rate = "<<std::setw(8)<<accept_good_rate;
            std::cout<<"AB rate = "<<std::setw(8)<<accept_bad_rate;
            std::cout<<"RB rate = "<<std::setw(8)<<reject_bad_rate;
            std::cout<<"T = "<<std::setw(10)<<cur_t;
            std::cout<<"current cost = "<<std::setw(12)<<cur_e;
            std::cout<<"best cost = "<<std::setw(12)<<m_best_e<<std::endl;
        }

        cur_t *= m_descent_rate;
        ++m_iter;
        total_accept_good += local_ag;
        total_accept_bad += local_ab;
        total_reject_bad += local_rb;
        local_ag = local_ab = local_rb = 0;
        e_sum = 0.0;
    }
    m_runtime = (clock()-run_beg)/CLOCKS_PER_SEC;
}

void line(int w1, int w2){
    std::cout<<"+";
    for(int i=0;i<w1;++i)
        std::cout<<"-";
    std::cout<<"+";
    for(int i=0;i<w2;++i)
        std::cout<<"-";
    std::cout<<"+"<<std::endl;
}

void SA::showReport(){
    int total_it = total_accept_good + total_accept_bad + total_reject_bad;
    int w1 = 17;
    int w2 = 12;
    std::cout<<"==========Final Result=========="<<std::endl;
    line(w1,w2);
    std::cout<<"|"<<std::left<<std::setw(w1)<<"Final energy"<<"|"<<std::left<<std::setw(w2)<<m_best_e<<"|"<<std::endl;
    line(w1,w2);
    std::cout<<"|"<<std::left<<std::setw(w1)<<"Total iteration"<<"|"<<std::left<<std::setw(w2)<<m_iter<<"|"<<std::endl;
    line(w1,w2);
    std::cout<<"|"<<std::left<<std::setw(w1)<<"Runtime(s)"<<"|"<<std::left<<std::setw(w2)<<m_runtime<<"|"<<std::endl;
    line(w1,w2);
    std::cout<<"|"<<std::left<<std::setw(w1)<<"Accept good rate"<<"|"<<std::left<<std::setw(w2)<<(double)total_accept_good/total_it<<"|"<<std::endl;
    line(w1,w2);
    std::cout<<"|"<<std::left<<std::setw(w1)<<"Accept bad rate"<<"|"<<std::left<<std::setw(w2)<<(double)total_accept_bad/total_it<<"|"<<std::endl;
    line(w1,w2);
    std::cout<<"|"<<std::left<<std::setw(w1)<<"Reject bad rate"<<"|"<<std::left<<std::setw(w2)<<(double)total_reject_bad/total_it<<"|"<<std::endl;
    line(w1,w2);
    std::cout<<"================================"<<std::endl;
}

double SA::getEnergy(){
    return m_libpy.attr("getEnergy")().cast<double>();
}

void SA::reverse(){
    m_libpy.attr("reverse")();    
}

void SA::jumpState(double scale, double cur_t, int iter){
    m_libpy.attr("jumpState")(scale,cur_t,iter);
}

void SA::storeBest(){
    m_libpy.attr("storeBest")();
}

void SA::output(){
    m_libpy.attr("output")();
}

bool SA::stopCondition(double cur_t,int iter, double ag_r, double ab_r, double rb_r, double best_e){
    return m_libpy.attr("stopCondition")(m_final_t,m_energy,cur_t,iter,ag_r,ab_r,rb_r,best_e).cast<bool>();
}

void SA::writeHistory(std::string file_name){
    std::ofstream fout{file_name};
    fout <<"iteration,current energy,average energy,temperature,lowest energy,accept good rate,accept bad rate,reject rate,time period" << std::endl;
    for(size_t i=0;i<records.size();++i){
        record & r = records.at(i);
        fout << r.iteration << "," << r.current_energy << "," 
            << r.average_energy << "," << r.temperature << "," 
            << r.best_energy << "," << r.good_accept_rate << "," 
            << r.bad_accept_rate << "," << r.reject_rate << "," 
            << r.period << std::endl;
    }
    fout.close();
}

void SA::plot(){
    std::vector<int>it;
    std::vector<double>e;
    std::vector<double>ave_e;
    std::vector<double>best_e;
    for(size_t i=0;i<records.size();++i){
        record &r = records[i];
        it.push_back(r.iteration);
        e.push_back(r.current_energy);
        ave_e.push_back(r.average_energy);
        best_e.push_back(r.best_energy);
    }
    py::object plt = py::module::import("matplotlib.pyplot");
    plt.attr("figure")("figsize"_a=*py::make_tuple(6,4),"facecolor"_a="#FFFFFF");
    plt.attr("title")("result");
    plt.attr("xlim")(0,m_iter);
    plt.attr("xlabel")("iter");
    plt.attr("ylabel")("energy");
    plt.attr("plot")(it,e,"b-","label"_a="cur_e");
    plt.attr("plot")(it,ave_e,"g-","label"_a="ave_e");
    plt.attr("plot")(it,best_e,"r-","label"_a="best_e");
    plt.attr("legend")();
    plt.attr("show")();
}

PYBIND11_MODULE(_sa, m){
    m.doc() = "SAAF";
    py::class_<SA>(m,"SA")
        .def(py::init<py::object>())
        .def("getEnergy",&SA::getEnergy)
        .def("setParam",&SA::setParam)
        .def("acceptance",&SA::acceptance)
        .def("run",&SA::run)
        .def("writeHistory",&SA::writeHistory)
        .def("output",&SA::output)
        .def("showReport",&SA::showReport)
        .def("plot",&SA::plot);
}
