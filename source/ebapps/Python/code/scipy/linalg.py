import numpy as np
from scipy import linalg

A = np.array([[1,2],[3,4]])
print A

print "Applying Inverse of A"
print linalg.inv(A)
