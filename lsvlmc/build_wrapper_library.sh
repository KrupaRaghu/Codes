g++ -L/nethome/afischer/BA/lsvlm/lib/ -llm -fPIC -Wall -I/nethome/afischer/BA/lsvlm/src/language_models/ -I/nethome/afischer/BA/lsvlm/src/ -I/nethome/afischer/BA/lsvlm/src/util/ -g -c lsvlm_c_bindings.cpp -o a.o
g++ -L/nethome/afischer/BA/lsvlm/lib/ -fPIC -llm -shared -Wl,-soname=lsvlm_c_bindings.so.1 -o lsvlm_c_bindings.so.1.0.1 a.o # fac.o
