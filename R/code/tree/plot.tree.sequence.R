library(tree)
data(cpus, package="MASS")
cpus.ltr <- tree(log(perf) ~ syct + mmin + mmax + cach + chmin + chmax, data = cpus)
plot(prune.tree(cpus.ltr))
