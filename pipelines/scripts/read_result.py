"""
Usage:
	read_result.py <file>
"""
from docopt import docopt
from json import loads
from pprint import pprint

def main():
	a = docopt(__doc__, version="0.1a")
	with open(a["<file>"], "r") as f:
		x = loads(f.read())
		#T_setup = x[-3]
		#T_gen = x[-2]
		#T_total = x[-1]
	#print "Total time", str(T_total), " - setup", str(T_setup), "- generation", str(T_gen)
	print "TIME -", x[1], x[2], x[3]
	for i,line in enumerate(x[0]):
		print "RANK %d" %(i + 1)
		print 'Sentence: "'+" ".join(map(lambda x: " ".join(x),line[1][0]))+'"'
		print "Total score", line[0], ":", line[1][2], "(len score),", line[1][3], "(lm score),", line[1][4], "(cond score),", line[1][5], "(pa_score)"
	
if __name__ == "__main__":
	main()
