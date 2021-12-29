CXX := g++
CXXFLAGS := -O3 -Wall -shared -std=c++17 -fPIC
TARGET = _sa.*.so

all: $(TARGET)

$(TARGET): _sa.cpp _sa.hpp
	$(CXX) $(CXXFLAGS) `python3 -m pybind11 --includes` $< -o _sa`python3-config --extension-suffix` `python3-config --includes`

.PHONY: clean run test

run: 
	python3 main.py 0.7 testbench/ami33/ami33.block testbench/ami33/ami33.nets output.txt

test:
	python3 test.py 0.7 testbench/ami33/ami33.block testbench/ami33/ami33.nets output.txt
	./verifier 0.7 testbench/ami33/ami33.block testbench/ami33/ami33.nets output.txt



clean: 
	rm -rf *.o *.so __pycache__ .pytest_cache *.txt *.csv *.HPWL */__pycache__/
