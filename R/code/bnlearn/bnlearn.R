# https://cran.r-project.org/web/packages/bnlearn/bnlearn.pdf
library(bnlearn)
data(learning.test)
## Simple learning
# first try the Grow-Shrink algorithm
res = gs(learning.test)
# plot the network structure.
plot(res)
# now try the Incremental Association algorithm.
res2 = iamb(learning.test)
# plot the new network structure.
plot(res2)
# the network structures seem to be identical, don't they?
all.equal(res, res2)
# how many tests each of the two algorithms used?
ntests(res)
ntests(res2)
# and the unoptimized implementation of these algorithms?
## Not run: ntests(gs(learning.test, optimized = FALSE))
## Not run: ntests(iamb(learning.test, optimized = FALSE))
## Greedy search
res = hc(learning.test)
plot(res)
## Another simple example (Gaussian data)
data(gaussian.test)
# first try the Grow-Shrink algorithm
res = gs(gaussian.test)
plot(res)
## Blacklist and whitelist use
# the arc B - F should not be there?
blacklist = data.frame(from = c("B", "F"), to = c("F", "B"))
blacklist
res3 = gs(learning.test, blacklist = blacklist)
plot(res3)
# force E - F direction (E -> F).
whitelist = data.frame(from = c("E"), to = c("F"))
whitelist
res4 = gs(learning.test, whitelist = whitelist)
plot(res4)
# use both blacklist and whitelist.
res5 = gs(learning.test, whitelist = whitelist, blacklist = blacklist)
plot(res5)
## Debugging
# use the debugging mode to see the learning algorithms
# in action.
res = gs(learning.test, debug = TRUE)
res = hc(learning.test, debug = TRUE)
# log the learning process for future reference.
## Not run:
sink(file = "learning-log.txt")
res = gs(learning.test, debug = TRUE)
sink()
# if something seems wrong, try the unoptimized version
# in strict mode (inconsistencies trigger errors):
res = gs(learning.test, optimized = FALSE, strict = TRUE, debug = TRUE)
# or disable strict mode to let the algorithm fix errors on the fly:
res = gs(learning.test, optimized = FALSE, strict = FALSE, debug = TRUE)
## End(Not run)
