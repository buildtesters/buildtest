library(gam)
y ~ Age + lo(Start)
# fit Start using a loess smooth with a (default) span of 0.5.
y ~ lo(Age) + lo(Start, Number)
y ~ lo(Age, span=0.3) # the argument name span cannot be abbreviated.

