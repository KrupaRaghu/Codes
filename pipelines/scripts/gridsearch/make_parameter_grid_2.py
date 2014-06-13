
paramnames = ["_dDocZero::Weight[0]", "_dDocZero::Weight[1]"]
print " ".join(paramnames)

#Resolution: 1%
for a in xrange(101):
    b = 100 - a
    print float(a)/100, float(b)/100
