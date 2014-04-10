"""
Usage:
	make_parameter_grid_full.py <resolution> [--phrases]
"""
from docopt import docopt
from itertools import product

def main():
	a = docopt(__doc__, version="0.1a")
	resolution = int(a["<resolution>"])
	paramnames = ["sentence_length::mean", "sentence_length::std_dev", "csel::epsilon", "phrase::epsilon", "LM::beta", "LM::w_dDoc", "LM::w_dImg", "LM::w_dMix", "LM::w_Zero"]
	print " ".join(paramnames)

	s_lengths = [11, 12, 13, 14]
	s_vars = []
	#csel_epsilons = [1e-5, 1e-4, 1e-3]
	csel_epsilons = [1e-5, 1e-3]
	#phrase_epsilons = [1e-5, 1e-4, 1e-3]
	phrase_epsilons = [0.0]
	if a["--phrases"]:
		phrase_epsilons = [1e-5, 1e-3]
	beta_FMA = [0.5, 0.6, 0.7, 0.8, 0.9]

	w_Zero_max = 5
	
	for (s, c, p, b) in product(s_lengths, csel_epsilons, phrase_epsilons, beta_FMA):
		for Z in xrange(0,w_Zero_max+1, resolution):
			for D in xrange(101 - Z):
			    for I in xrange(0, 101-D-Z, resolution):
				M = 100-Z-D-I
				print s, c, p, b, -b, 1.0, float(D)/100, float(I)/100, float(M)/100, float(Z)/100

if __name__ == "__main__":
	main()

