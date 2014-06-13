
paramnames = ["_DocumentTrigram_main::Weight[0]", "_DocumentTrigram_main::Weight[1]"]
print " ".join(paramnames)

#Resolution: 1%
for a in xrange(101):
    print float(a)/100, float(100-a)/100
