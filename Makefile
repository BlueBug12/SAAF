CXX := g++
CXXFLAGS := -O3 -Wall -shared -std=c++11 -fPIC
TARGET = _sa.*.so

all: $(TARGET)

$(TARGET): _sa.cpp _sa.hpp
	$(CXX) $(CXXFLAGS) `python3 -m pybind11 --includes` $< -o _sa`python3-config --extension-suffix` `python3-config --includes`

test: sa.py
	python3 -m pytest sa.py

.PHONY: clean
clean: 
	rm -rf *.o *.so __pycache__ .pytest_cache
