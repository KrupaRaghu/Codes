"""
Usage:
	make_parameter_grid_epsilon.py <vocabsize>
"""
from docopt import docopt
from itertools import product

def main():
	a = docopt(__doc__, version="0.1a")
	paramnames = ["epsilon", "vocsize"]
	vsize = int(a["<vocabsize>"])

	print " ".join(paramnames)

	eps = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1]

	for e in eps:
		print e, vsize

if __name__ == "__main__":
	main()

