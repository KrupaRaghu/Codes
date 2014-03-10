from ..experiment_config import *
from ..formats.Sentences import *
#Functions for generating captions.

BEAM_SIZE = 500

class CaptionGenerator(object):
    def __init__(self, lang_model, len_model, csel_model, pa_model = None):
        self.lang_model = lang_model
        self.len_model = len_model
        self.csel_model = csel_model
        self.pa_model = pa_model
    
    def score_sentence(self, sentence, verbose = False):
        text = sentence.get_text(one_per_line = False)
        lm_prob, lm_score = self.lang_model.AssessText(text)
        cond_score = sum(map(lambda x: self.csel_model(x), text.split()))
        phrase_score = 0.0
        if not pa_model is None:
            for i in xrange(len(sentence)-1):
                phrase_score = self.pa_model(sentence[i], sentence[i+1])
        len_score = self.len_model(len(text.split()))
        if verbose:
            return lm_score, cond_score, len_score, phrase_score
        else:
            total_score = lm_score + cond_score + len_score + phrase_score
            return total_score

def generate_captions(units, len_model, csel_model, lang_model, pa_model = None):
    curr_cand = [[SENTENCE_START]]
    next_cand = []
    


    pass
