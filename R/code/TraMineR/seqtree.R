library(TraMineR)
data(mvad)
## Defining a state sequence object
mvad.seq <- seqdef(mvad[, 17:86])
## Growing a seqtree from Hamming distances:
## Warning: The R=10 used here to save computation time is
## much too small and will generate strongly unstable results.
## We recommend to set R at least as R=1000.
## To comply with this small R value, we set pval = 0.1.
seqt <- seqtree(mvad.seq~ male + Grammar + funemp + gcse5eq + fmpr + livboth,
data=mvad, R=10, pval=0.1, seqdist.arg=list(method="HAM", norm="auto"))
print(seqt)
## Growing a seqtree from an existing distance matrix
mvad.dhd <- seqdist(mvad.seq, method="DHD")
seqt <- seqtree(mvad.seq~ male + Grammar + funemp + gcse5eq + fmpr + livboth,
data=mvad, R=10, pval=0.1, diss=mvad.dhd)
print(seqt)
### Following commands only work if GraphViz is properly installed
## Not run:
seqtreedisplay(seqt, type="d", border=NA)
seqtreedisplay(seqt, type="I", sortv=cmdscale(mvad.dhd, k=1))
## End(Not run)
