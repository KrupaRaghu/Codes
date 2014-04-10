"""
Usage:
	normalize_content_selection_lowercase.py <modelfile>
"""
from docopt import docopt
from pipelines.formats.ConditionalContentSelection import ConditionalContentSelector
from collections import Counter, defaultdict

def main():
	a = docopt(__doc__, version="0.1a")
	
	counts = defaultdict(lambda: Counter({}))
	totals = Counter({}) 
	f = open(a["<modelfile>"], "r")
	model = ConditionalContentSelector.decode(f.read())
	for k,v in model.counts.iteritems():
		counts[k.lower()].update(v)
	for k,v in model.totals.iteritems():
		totals.update(Counter({k.lower():v}))
	totalmodel = ConditionalContentSelector(counts, totals)
	print totalmodel.encode()	

if __name__ == "__main__":
	main()
