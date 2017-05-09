from funcsigs import signature
def test(a,b):
	pass

sig = signature(test)

print str(sig)

print str(sig.parameters['b'])

print sig.parameters['b'].annotation


