class pLDADocument(list):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self.total = sum(self)

    def get_topic_distribution(self):
        return map(lambda x: x/self.total, self)

    def get_topic_proportion(self, topic):
        return self[topic]/self.total

    def encode(self):
        return " ".join(map(str, self))

    @staticmethod
    def decode(string):
        return pLDADocument(map(float, string.split()))

class pLDAModel(object):
    def __init__(self, topicdict):
        self.t_dict = topicdict
        self.t_totals = self.count_topic_totals()

    def get_num_topics(self):
        return len(self.t_totals)

    def count_topic_totals(self):
        totals = [0]*len(self.t_dict.items()[0][1])
        for word, t_dist in self.t_dict.iteritems():
            for i in xrange(len(t_dist)):
                totals[i] = totals[i]+t_dist[i]
        return totals
    
    def get_prob(self, word, topic):
        cnt = 0
        if len(self.t_dict.get(word,[])) >= topic:
            cnt = self.t_dict.get(word, [])[topic]
        return float(cnt)/self.t_totals[topic]

    def get_word_dist_over_topics(self, word):
        return map(lambda (c,t):float(c)/t, zip(self.t_dict.get(word, [0]*self.get_num_topics()),self.t_totals))

    @staticmethod
    def decode(string):
        if string.__class__ == str:
            string = string.decode("utf-8")
        entries = string.split(u"\n")
        t_dict = {}
        for entry in entries:
            if not entry:
                continue
            word = entry.split(u"\t", 1)[0]
            wlist = entry.split(u"\t", 1)[1]
            t_dict[word] = map(int, wlist.split())
        return pLDAModel(t_dict)

    def encode(self):
        return u"\n".join(map(lambda (w,tw): w+u"\t"+u" ".join(map(str, tw))))

class pLDACorpus(list):
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)

    @staticmethod
    def decode(text):
        content = []
        for line in text.split("\n"):
            bow_cont = []
            line = line.split()
            for i in xrange(len(line)/2):
                word = line[i*2]
                count = int(line[i*2+2])
                bow_cont.append((word, count))
            content.append(BoW(bow_cont))
        return pLDACorpus(content)

    def encode(self):
        outlines = []
        for D in self:
            newline = []
            for (k,v) in D.iteritems():
                if k.__class__ == str:
                    newline.append(k.decode("utf-8"))
                else:
                    newline.append(k)
                newline.append(unicode(v))
            outlines.append(u' '.join(newline))
        return u'\n'.join(outlines).encode("utf-8")
