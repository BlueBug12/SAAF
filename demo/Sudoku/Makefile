CXX := g++
CXXFLAGS := -O3 -Wall -shared -std=c++17 -fPIC
TARGET = _sa.*.so

all: $(TARGET)

$(TARGET): _sa.cpp _sa.hpp
	$(CXX) $(CXXFLAGS) `python3 -m pybind11 --includes` $< -o _sa`python3-config --extension-suffix` `python3-config --includes`

.PHONY: clean test run
run: 
	python3 main.py testbench/s1.txt

test:
	python3 -m pytest test.py testbench/s1.txt
	python3 -m pytest test.py testbench/s2.txt
	python3 -m pytest test.py testbench/empty.txt

clean: 
	rm -rf *.o *.so __pycache__ .pytest_cache *.txt *.csv */__pycache__/
