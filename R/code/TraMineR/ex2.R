library(TraMineR)
data(ex2)
ex2w.seq <- seqdef(ex2.weighted, 1, weights=ex2.weighted$weight)
ex2u.seq <- seqdef(ex2.unweighted)
