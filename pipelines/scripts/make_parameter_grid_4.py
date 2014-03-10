
paramnames = ["Weight[0]", "Weight[1]", "Weight[2]", "Weight[3]"]
print " ".join(paramnames)

#Resolution: 1%
for a in xrange(101):
    for b in xrange(101-a):
        for c in xrange(101-a-b):
            d = 100 - a - b - c
            print float(a)/100, float(b)/100, float(c)/100, float(d)/100
