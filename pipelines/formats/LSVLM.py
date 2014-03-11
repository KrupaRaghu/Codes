from ..experiment_config import LSVLM_LIB_PATH, LSVLM_WRAPPER_PATH
from ..formats.Vocabulary import *
from math import exp
from data_manager.OSM import object_from_file
from cffi import *

# LSVLM wrapper class. Contains the ffi-opened library wrappers as well as a factory, thus defining a scope.
class LSVLMWrapper(object):
    def __init__(self, lsvlmlibpath, wrapperpath):
        self.ffi = FFI()
        #Setup - function definitions
        #LMFactory
        self.ffi.cdef('void* new_LMFactory();')
        self.ffi.cdef('void* LMFactory_StartLM(void* factory, char* lm_name, void* V);')
        #Vocabularies
        self.ffi.cdef('void* new_Vocabulary(char* filename);')
        #DynParams
        self.ffi.cdef('void* new_DynParams();')
        self.ffi.cdef('void DynParams_SetParameter(void* params, char* Identifier, float Value);')
        self.ffi.cdef('void DynParams_SetParameterForLM(void* LM, void* params, char* Identifier, float Value);')
        self.ffi.cdef('int DynParams_ExistsParameter(void* params, char* LMName, char* parIdentifier);')

        self.ffi.cdef('float DynParams_RealParameter(void* params, char* Identifier);')
        self.ffi.cdef('float DynParams_RealParameterForLM(void* params, void* lm, char* Identifier);')
        #LMs
        self.ffi.cdef('void* new_LM(void* fac, char* name, void* V);')
        self.ffi.cdef('double LM_Prob(void* lm, int* Hist, int M);')
        self.ffi.cdef('double LM_Score(void* lm, int* Hist, int M);')
        self.ffi.cdef('double LM_Update(void* lm, int *Doc, int M, char* Key);')
        self.ffi.cdef('void LM_CollectParams(void* lm, void* params);')
        self.ffi.cdef('void LM_ReInit(void* lm, void* params);')

        self.lsvlm = self.ffi.dlopen(lsvlmlibpath, self.ffi.RTLD_LAZY + self.ffi.RTLD_GLOBAL)
        self.wrapper = self.ffi.dlopen(wrapperpath, self.ffi.RTLD_LAZY)

        #Instantiate factory
        self.factory = self.wrapper.new_LMFactory()
   
    def NewVocabulary(self, vocabulary_filepath):
        vocpath_wrap = self.ffi.new("char[]", vocabulary_filepath)
        return self.wrapper.new_Vocabulary(vocpath_wrap)
    
    def NewDynParams(self):
        return self.wrapper.new_DynParams()

    def StartLM(self, LMfile, vocfile):
        voc = self.NewVocabulary(vocfile)
        lmfile = self.ffi.new("char[]", LMfile)
        return self.wrapper.LMFactory_StartLM(self.factory, lmfile, voc)

LSVLM = LSVLMWrapper(LSVLM_LIB_PATH, LSVLM_WRAPPER_PATH)

class LSVLM(object):
    def __init__(self, lmfile = None, config = None, vocfile = None):
        self.LM = None
        self.updates = []
        if lmfile is None:
            self.lmfile = None
            self.set_config(config)
            self.set_vocabulary(vocfile)
        else:
            lmname, config_file, vocfile_file, lmfile_file = LSVLM.parse_lmfile(lmfile)
            from sys import stderr
            stderr.write( "LMfile %s exists, initializing from that file.\n" % (lmfile))
            if lmfile_file is None:
                self.set_lmfile(lmfile)
            else:
                self.set_lmfile(lmfile_file)
            if vocfile_file is None:
                self.set_vocabulary(vocfile)
            else:
                self.set_vocabulary(vocfile_file)
            self.set_config(config_file)

    def start(self, libwrapper = LSVLM):
        self.lib = libwrapper
        if not self.LM is None:
            #LM already started, do nothing
            return
        from os.path import isfile
        if self.vocfile is None or not isfile(self.vocfile):
            raise TypeError("LM %s does not yet have a vocabulary. Instantiation impossible." % (self.get_lmname()))
        if self.lmfile is None or not isfile(self.lmfile):
            raise TypeError("LMfile %s does not exist. Instantiation impossible." % (self.lmfile))
        #Start the LM: save pointer from library wrapper. The LM can then finally be used.
        self.LM = self.lib.StartLM(self.lmfile, self.vocfile)
    
    #Actual LM wrapper functions. LM must have been started in order to use these.
    def Update(self, hist, M, key):
        hist = self.lib.ffi.new("int[]", hist)
        res = self.lib.wrapper.LM_Update(self.lm, hist, M, key)
        res = self.lib.ffi.cast("int", res)
        return res

    def Prob_words(self, hist, M):
        return self.Prob(self.voc.index_words(hist), M)

    def Score_words(self, hist, M):
        return self.Score(self.voc.index_words(hist), M)

    def Prob(self, hist, M):
        hist = self.lib.ffi.new("int[]", hist)
        p = self.lib.wrapper.LM_Prob(self.LM, hist, length)
        p = self.lib.ffi.cast("double", p)
        return float(p)

    def Score(self, hist, length):
        hist = self.lib.ffi.new("int[]", hist)
        p = self.lib.wrapper.LM_Score(self.LM, hist, length)
        p = self.lib.ffi.cast("double", p)
        return float(p)

    def AssessText(self, sent, M):
        score = 0.0
        for i in xrange(len(sent)-M):
            score = score + self.Score_words(sent[i:i+M], M)
        return exp(-score), score

    def Perplexity(self, sent, M):
        prob, score = self.AssessText(sent, M)
	if prob > 0.0:
        	return pow(prob, -1.0/len(sent))
	else:
		return float("inf")

    #Auxiliary function for setting update parameters for ReInit
    def add_DynParam(self, paramname, paramval):
        self.updates.append((paramname, paramval))

    def ReInit(self):
        #Build DynParams object
        dynparams = self.lib.wrapper.new_DynParams()
        #Fill with all pending updates
        for (paramname, paramval) in self.updates:
            name_ffi = self.lib.ffi.new("char[]", paramname)
            self.lib.wrapper.DynParams_SetParameterForLM(self.LM, dynparams, name_ffi, paramval)
        #Send to LM via ReInit
        self.lib.wrapper.LM_ReInit(self.LM, dynparams)
        self.updates = []

    def set_vocabulary(self, vocfile):
        self.vocfile = vocfile
        if not self.vocfile is None:
            self.voc = object_from_file(Vocabulary, vocfile)
        else:
            self.voc = None
    def set_config(self, config):
        self.config = []
        if not config is None:
            for line in config:
                if line.__class__ == str:
                    self.config.append(line.decode('utf-8'))
                else:
                    self.config.append(line)
    def set_lmfile(self, lmfile):
        self.lmfile = lmfile
    def get_lmname(self):
        for line in self.config:
            if line.startswith("MainLM"):
                return line.split()[-1]

    @staticmethod
    def init_from_lmfile(lmfile):
        lmname, config, voc, lmfile_infile = LSVLM.parse_lmfile(lmfile)
        from os.path import samefile
        if not samefile(lmfile, lmfile_infile):
            from sys import stderr
            stderr.write("Warning: LM in file %s encodes a different LMfile %s!" % (lmfile, lmfile_infile))
        return LSVLM(lmfile = lmfile, config = config, vocfile = voc)
    @staticmethod
    def parse_lmfile(lmfile):
        with open(lmfile, "r") as f:
            return LSVLM.parse_lm_lines(f.readlines())
    @staticmethod
    def parse_lm_lines(lines):
        voc = None
        lmname = None
        lmfile = None
        config = []
        in_comment = False
        for line in lines:
            if line.startswith("MainLM"):
                lmname = line.split()[-1]
            if in_comment:
                if line.startswith("LMFile"):
                    lmfile = line.split()[-1]
                if line.startswith("DefaultVocabulary"):
                    voc = line.split()[-1]
            else:
                config.append(line)
            if line.startswith("# Comments"):
                in_comment = True
        return lmname, config, voc, lmfile
    @staticmethod
    def decode(content, filename=None):
        lmname, config, vocfile, lmfile = LSVLM.parse_lm_lines(content.split("\n"))
        if lmfile is None and not filename is None:
            from os.path import abspath
            lmfile = abspath(filename)
        return LSVLM(lmfile = lmfile, config=config, vocfile=vocfile)
    def encode(self, filename):
        comments = []
        if not self.vocfile is None:
            comments.append(u"DefaultVocabulary %s" % (self.vocfile))
        if not self.lmfile is None:
            comments.append(u'LMFile %s' % (self.lmfile))
        out = u'\n'.join(self.config + u'# Comments %d' % (len(comments)) + comments)
        return out.encode('utf-8')
