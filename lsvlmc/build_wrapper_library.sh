g++ -L/home/janno/DREENE/lsvlm/lib/ -llm -fPIC -Wall -I/home/janno/DREENE/lsvlm/src/language_models/ -I/home/janno/DREENE/lsvlm/src/ -I/home/janno/DREENE/lsvlm/src/util/ -g -c lsvlm_c_bindings.cpp -o a.o
g++ -L/home/janno/DREENE/lsvlm/lib/ -fPIC -llm -shared -Wl,-soname=lsvlm_c_bindings.so.1 -o lsvlm_c_bindings.so.1.0.1 a.o # fac.o
