from cffi import FFI

from src.definitions import LSVLM_LIB_PATH, LSVLM_WRAPPER_PATH

class LSVLM(object):
    def __init__(self, lmfile, vocfile):
        self.ffi = FFI()
        #Setup
        self.ffi.cdef('void* new_LMFactory();')
        self.ffi.cdef('void* new_Vocabulary(char* filename);')
        self.ffi.cdef('void* new_LM(void* fac, char* name, void* V);')
        self.ffi.cdef('double LM_Prob(void* lm, int* Hist, int M);')
        self.lsvlm = ffi.dlopen(LSVLM_LIB_PATH, self.ffi.RTLD_LAZY + self.ffi.RTZL_GLOBAL)
        self.wrapper = ffi.dlopen(LSVLM_WRAPPER_PATH, self.ffi.RTLD_LAZY)
        #Instantiate factory
        self.factory = test.new_LMFactory()
        
        #Instantiate Vocabulary
        vocname = self.ffi.new("char[]", vocfile)
        self.voc = self.wrapper.new_Vocabulary(vocname)
        #Instantiate LM
        lmname = self.ffi.new("char[]", lmfile)
        self.lm = self.wrapper.new_LM(fac, lmname, self.voc)

    def Update(self, hist, M, key):
        hist = self.ffi.new("int[]", hist)
        res = self.wrapper.LM_Update(self.lm, hist, M, key)
        res = self.ffi.cast("int", res)
        return res

    def Prob(self, hist, M):
        hist = self.ffi.new("int[]", hist)
        p = self.wrapper.LM_Prob(lm, hist, length)
        p = self.ffi.cast("double", p)
        return float(p)

    def Score(hist, length):
        hist = self.ffi.new("int[]", hist)
        p = self.wrapper.LM_Score(lm, hist, length)
        p = self.ffi.cast("double", p)
        return float(p)

class LMWrapper(object):
    def __init__(self, lsvlmlibpath, wrapperpath):
        self.ffi = FFI()
        #Setup
        self.ffi.cdef('void* new_LMFactory();')
        self.ffi.cdef('void* new_Vocabulary(char* filename);')
        self.ffi.cdef('void* new_LM(void* fac, char* name, void* V);')
        self.ffi.cdef('double LM_Prob(void* lm, int* Hist, int M);')
        self.lsvlm = ffi.dlopen(lsvlmlibpath, self.ffi.RTLD_LAZY + self.ffi.RTZL_GLOBAL)
        self.wrapper = ffi.dlopen(wrapperpath, self.ffi.RTLD_LAZY)

        #Instantiate factory
        self.factory = test.new_LMFactory()
    
    def makeScoreLM(self, lmfile, vocfile):
        #Instantiate vocabulary
        vocname = self.ffi.new("char[]", vocfile)
        voc = self.wrapper.new_Vocabulary(vocname)

        #Instantiate LM
        lmname = self.ffi.new("char[]", lmfile)
        lm = self.wrapper.new_LM(fac, lmname, voc)
        
        def score(hist, length):
            hist = self.ffi.new("int[]", hist)
            p = self.wrapper.LM_Score(lm, hist, length)
            p = self.ffi.cast("double", p)
            return float(p)
        return score

    def makeProbLM(self, lmfile, vocfile):
        #Instantiate vocabulary
        vocname = self.ffi.new("char[]", vocfile)
        voc = self.wrapper.new_Vocabulary(vocname)

        #Instantiate LM
        lmname = self.ffi.new("char[]", lmfile)
        lm = self.wrapper.new_LM(fac, lmname, voc)
        
        def prob(hist, length):
            hist = self.ffi.new("int[]", hist)
            p = self.wrapper.LM_Prob(lm, hist, length)
            p = self.ffi.cast("double", p)
            return float(p)
        return prob
