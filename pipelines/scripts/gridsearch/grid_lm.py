


resolution = 1
paramnames = ["_FL_FMA_standard::Weight[0]", "_FL_FMA_standard::Weight[1]", "_FL_FMA_standard::Weight[2]", "_AllLDAZero::Weight[0]", "_AllLDAZero::Weight[1]", "_AllLDAZero::Weight[2]", "_AllLDAZero::Weight[3]"]
print " ".join(paramnames)
betas_FMA = [0.5]#, 0.6, 0.7, 0.8, 0.9]

w_Zeros = [1,2,3,4,5]

for beta in betas_FMA:
	for Z in w_Zeros:
		for D in xrange(16, 27, resolution):
			for I in xrange(0, 6, 1):
				M = 100-Z-D-I
				print beta, -beta, 1.0, float(D)/100, float(I)/100, float(M)/100, float(Z)/100

