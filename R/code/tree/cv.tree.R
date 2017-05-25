library(tree)
data(cpus, package="MASS")
cpus.ltr <- tree(log10(perf) ~ syct + mmin + mmax + cach
+ chmin + chmax, data=cpus)
cv.tree(cpus.ltr, , prune.tree)
