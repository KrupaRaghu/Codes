SENTENCE_START = "<S_START>"

def _get_M_list_for_sentence(sent, M):
        m_cur = 0
	M_list = []
        for i in xrange(len(sent)):
	    if m_cur < M:
		m_cur = m_cur + 1
            if sent[i] == SENTENCE_START:
                m_cur = 1
	    M_list.append(m_cur)
	return M_list

sentence = [SENTENCE_START, '1', '2', '3', '4', SENTENCE_START, SENTENCE_START, "3", "4", SENTENCE_START]
Ms = _get_M_list_for_sentence(sentence, 3)
print zip(sentence, Ms)
for m, i in zip(Ms, xrange(len(sentence))):
	print m, i, sentence[i-m + 1:i + 1]
