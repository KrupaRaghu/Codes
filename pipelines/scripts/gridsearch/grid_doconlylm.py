
resolution = 5
paramnames = ["_dDocZero::Weight[0]", "_dDocZero::Weight[1]"]
print " ".join(paramnames)

for Z in xrange(0,101, resolution):
	D = 100-Z
	print float(D)/100, float(Z)/100

