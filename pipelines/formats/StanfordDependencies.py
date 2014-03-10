import re
from pprint import pprint
from json import loads, dumps

#A class to contain Stanford dependencies.

#Function for parsing the typedDependencies output of the Stanford Parser.
TYPED_DEPS_REGEXP=r"([^(,\s)]+)"
WORD_TAG_POS_RE=r"(.+)/([A-Z]+)-([0-9]+)"

NOUNS = ['NN', 'NNS', 'NP', 'NPS', 'NNP']
PREPOSITIONS = ['IN']
VERBS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
OTHER_ALLOWED_TAGS_FULL = ['DT', 'CD', 'JJ', 'JJR', 'JJS', 'TO', 'PRP']
OTHER_ALLOWED_TAGS = ['DT', 'JJ', 'JJR', 'JJS', 'CD']

ALLOWED_TAGS_HEADS = NOUNS + VERBS + PREPOSITIONS + OTHER_ALLOWED_TAGS_FULL
ALLOWED_TAGS_CONT = NOUNS + PREPOSITIONS + OTHER_ALLOWED_TAGS

ALLOWED_TYPES = []

class StanfordDependencies(object):
    def __init__(self, words, tags, deps):
        self.words = words[:]
        self.tags = tags[:]
        self.deps = deps[:]

    def __getitem__(self, i):
        entry = []
        for j, w in enumerate(self.words[i]):
            entry.append([self.words[i][j], self.tags[i][j], self.deps[i][j]])
        return entry

    @staticmethod
    def decode(string):
        c = string.split("\n")
        words_raw = loads(c[0])
        words = []
        for line in words_raw:
            nl = []
            for w in line:
                nl.append((w[0], w[1]))
            words.append(nl)
        return StanfordDependencies(words, loads(c[1]), loads(c[2]))

    def encode(self):
        return dumps(self.words)+"\n"+dumps(self.tags)+"\n"+dumps(self.deps)
