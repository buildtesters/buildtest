library(TraMineR)
data(famform)
famform.seq <- seqdef(famform)
## The LCP's length between sequences 1 and 2
## in the famform sequence object is 2
seqLLCP(famform.seq[1,],famform.seq[2,])
