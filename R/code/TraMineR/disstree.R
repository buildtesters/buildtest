library(TraMineR)
data(mvad)
## Defining a state sequence object
mvad.seq <- seqdef(mvad[, 17:86])
## Computing dissimilarities (any dissimilarity measure can be used)
mvad.ham <- seqdist(mvad.seq, method="HAM")
## Grow the tree using using a low R value for illustration.
## For R=10, pval cannot be lower than 0.1
dt <- disstree(mvad.ham~ male + Grammar + funemp + gcse5eq + fmpr + livboth,
data=mvad, R = 10, pval = 0.1)
print(dt)
## Will only work if GraphViz is properly installed
## See seqtree for simpler way to plot a sequence tree.
## Not run:
disstreedisplay(dt, image.fun = seqdplot, image.data = mvad.seq,
## Additional parameters passed to seqdplot
with.legend = FALSE, axes = FALSE, ylab = "")
## End(Not run)
## Second method, using a specific function
myplotfunction <- function(individuals, seqs, ...) {
par(font.sub=2, mar=c(3,0,6,0), mgp=c(0,0,0))
## using mds to order sequence in seqiplot
mds <- cmdscale(seqdist(seqs[individuals,], method="HAM"),k=1)
seqiplot(seqs[individuals,], sortv=mds,...)
}
## If image.data is not set, index of individuals are sent to image.fun
## Not run:
disstreedisplay(dt, image.fun = myplotfunction, cex.main = 3,
## additional parameters passed to myplotfunction
seqs = mvad.seq,
## additional parameters passed to seqiplot (through myplotfunction)
with.legend = FALSE, axes = FALSE, idxs = 0, space = 0, ylab = "", border = NA)
## End(Not run)
