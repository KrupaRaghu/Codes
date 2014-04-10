"""
Usage:
	make_parameter_grid_LM.py <resolution> <w_zero_max> <resolution_w_zero>
"""
from docopt import docopt
from itertools import product

def main():
	a = docopt(__doc__, version="0.1a")
	resolution = int(a["<resolution>"])
	resolution_zero = int(a["<resolution_w_zero>"])
	paramnames = ["_FL_FMA_standard::Weight[0]", "_FL_FMA_standard::Weight[1]", "_FL_FMA_standard::Weight[2]", "_AllLDAZero::Weight[0]", "_AllLDAZero::Weight[1]", "_AllLDAZero::Weight[2]", "_AllLDAZero::Weight[3]"]
	print " ".join(paramnames)
	betas_FMA = [0.5]#, 0.6, 0.7, 0.8, 0.9]

	w_Zero_max = int(a["<w_zero_max>"])
	

	for beta in betas_FMA:
		for Z in xrange(0,w_Zero_max+1, resolution_zero):
			for D in xrange(0, 101 - Z, resolution):
			    for I in xrange(0, 101-D-Z, resolution):
				M = 100-Z-D-I
				print beta, -beta, 1.0, float(D)/100, float(I)/100, float(M)/100, float(Z)/100

if __name__ == "__main__":
	main()

