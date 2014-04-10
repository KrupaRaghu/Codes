#Functions for computing the Translation Edit Rate between two sentences.

def Levenshtein_detailed(sent_hyp, sent_ref, COST_DEL = 1, COST_INS = 1, COST_SUB = 1):
	distance = []
    	for i in xrange(len(sent_hyp) + 1):
        	distance.append([])
		for j in xrange(len(sent_ref) + 1):
			if j == 0:
				distance[i].append((i,0,0,0))
			elif i == 0:
				distance[i].append((0,j,0,0))
			else:
				distance[i].append((0,0,0,0))
	for j in xrange(len(sent_ref)):
        	j = j + 1
		for i in xrange(len(sent_hyp)):
			i = i + 1
			if sent_hyp[i-1] == sent_ref[j-1]:
				distance[i][j] = distance[i-1][j-1]
			else:
				new_del = join(distance[i-1][j], (0, COST_DEL, 0,0))
				new_ins = join(distance[i][j-1] , (COST_INS, 0, 0, 0))
				new_subs = join(distance[i-1][j-1], (0,0, COST_SUB, 0))
				distance[i][j] = min([new_del, new_ins, new_subs], key=sum)

	return distance[-1][-1]

def join(a,b):
	return tuple(map(lambda (a,b): a+b, zip(a,b)))

#The first step is simply Levenshtein distance on words.
def Levenshtein_words(sent_hyp, sent_ref, COST_DEL = 1, COST_INS = 1, COST_SUB = 1):
    distance = []
    for i in xrange(len(sent_hyp) + 1):
        distance.append([])
        for j in xrange(len(sent_ref) + 1):
            if j == 0:
                distance[i].append(i)
            elif i == 0:
                distance[i].append(j)
            else:
                distance[i].append(0)
    for j in xrange(len(sent_ref)):
        j = j + 1
        for i in xrange(len(sent_hyp)):
            i = i + 1
            if sent_hyp[i-1] == sent_ref[j-1]:
                distance[i][j] = distance[i-1][j-1]
            else:
                distance[i][j] = min([distance[i-1][j] + COST_DEL, distance[i][j-1] + COST_INS, distance[i-1][j-1] + COST_SUB])

    return distance[-1][-1]

def generate_shifts(sent):
    #print sent
    #Generate all possible shifts for the given sentence.
    for l in range(1, len(sent)):
        #Try the size of the contiguous sequence to be shifted.
        #Must be > 0 and < len(sent)
        for offset in xrange(len(sent)-l+1):
            seq = sent[offset:offset+l]
            for shift_left in xrange(offset):
                shift_left = shift_left + 1
                ln_noshift = sent[0:offset-shift_left]
                ln_shift = sent[offset-shift_left:offset]
                rn = sent[offset+l:]
                shift_l = ln_noshift + seq + ln_shift + rn
                yield shift_l 

            for shift_right in xrange(len(sent) - offset - l):
                shift_right = shift_right + 1
                ln = sent[0:offset]
                rn_shift = sent[offset+l:offset+l+shift_right]
                rn_noshift = sent[offset+l+shift_right:]
                shift_r = ln+rn_shift+seq+rn_noshift
                yield shift_r 

#Minimum word edit distance when incorporating shifts.
def Levenshtein_shifts(sent_hyp, sent_ref, COST_SHIFT = 1, COST_INS = 1, COST_DEL = 1, COST_SUB=1):
    sent = sent_hyp[:]
    cur_cost = Levenshtein_detailed(sent_hyp, sent_ref)
    cur_total = sum(cur_cost)
    num_shifts = 0
    while(True):
        shifts = list(generate_shifts(sent))
        cur_cand = sorted(map(lambda x:(Levenshtein_detailed(x, sent_ref, COST_INS=COST_INS, COST_DEL=COST_DEL, COST_SUB=COST_SUB),x), generate_shifts(sent)), key=lambda (a,b): sum(a))
        if cur_total - sum(cur_cand[0][0]) <= 0:
            return cur_cost[0], cur_cost[1], cur_cost[2], cur_cost[3], num_shifts*COST_SHIFT
        else: 
            num_shifts = num_shifts + 1
            cur_cost, sent = cur_cand[0]
	    cur_total = sum(cur_cost)

#Finally, the TER method
def TER(sent_hyp, sent_ref, COST_SHIFT = 1, COST_INS = 1, COST_DEL = 1, COST_SUB=1, detailed=False):
	cost = Levenshtein_shifts(sent_hyp, sent_ref, COST_INS=COST_INS, COST_DEL=COST_DEL, COST_SUB=COST_SUB, COST_SHIFT=COST_SHIFT)
	total = sum(cost)
	if not detailed:
		return float(total)/len(sent_ref)
	else:
		return map(lambda x: float(x)/len(sent_ref), cost)

#Few tests
#print TER([1,2,3],[1,3,2])
#print TER([1,2,3],[1,3,2], detailed=True)
#print TER([1,3,2],[1,2,3])
#print TER([1,1,1],[2])
#print TER([6,1,2,3,4,5],[1,2,3,4,5,6])
#print TER([6,1,3,4,5,2],[1,2,3,4,5,6])
#Seems to work.
