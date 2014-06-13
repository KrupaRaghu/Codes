
resolution = 10
paramnames = ["_AllLDAZero::Weight[0]", "_AllLDAZero::Weight[1]", "_AllLDAZero::Weight[2]", "_AllLDAZero::Weight[3]"]
print " ".join(paramnames)

w_Zeros = [5]

for Z in w_Zeros:
	for D in xrange(0, 101, resolution):
		for I in xrange(0, 6, 1):
			M = 100-Z-D-I
			print float(D)/100, float(I)/100, float(M)/100, float(Z)/100

