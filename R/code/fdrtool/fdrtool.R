#https://cran.r-project.org/web/packages/fdrtool/fdrtool.pdf
# load "fdrtool" library and p-values
library("fdrtool")
data(pvalues)
# estimate fdr and Fdr from p-values
data(pvalues)
fdr = fdrtool(pvalues, statistic="pvalue")
fdr$qval # estimated Fdr values
fdr$lfdr # estimated local fdr
# the same but with black and white figure
fdr = fdrtool(pvalues, statistic="pvalue", color.figure=FALSE)
# estimate fdr and Fdr from z-scores
sd.true = 2.232
n = 500
z = rnorm(n, sd=sd.true)
z = c(z, runif(30, 5, 10)) # add some contamination
fdr = fdrtool(z)
# you may change some parameters of the underlying functions
fdr = fdrtool(z, cutoff.method="pct0", pct0=0.9)
