library(TraMineR)
## ========================
## Example without missings
## ========================
## Defining a sequence object with columns 10 to 25 of a
## subset of the 'biofam' data set
data(biofam)
biofam.seq <- seqdef(biofam[501:600, 10:25])
## OM distances with a substitution-cost matrix derived
## from transition rates
biofam.om <- seqdist(biofam.seq, method = "OM", indel = 3,
sm = "TRATE")
## OM distances using the vector of estimated indels and
## substitution costs derived from the estimated indels
costs <- seqcost(biofam.seq, method = "INDELSLOG")
biofam.om <- seqdist(biofam.seq, method = "OM",
indel = costs$indel, sm = costs$sm)
## Normalized LCP distances
biofam.lcp.n <- seqdist(biofam.seq, method = "LCP",
norm = "auto")
## Normalized LCS distances to the most frequent sequence
biofam.dref1 <- seqdist(biofam.seq, method = "LCS",
refseq = 0, norm = "auto")
## LCS distances to an external sequence
ref <- seqdef("(0,5)-(3,5)-(4,6)", informat = "SPS",
alphabet = alphabet(biofam.seq))
biofam.dref2 <- seqdist(biofam.seq, method = "LCS",
refseq = ref)
## Chi-squared distance over the full observed timeframe
biofam.chi.full <- seqdist(biofam.seq, method = "CHI2",
step = max(seqlength(biofam.seq)))
## Chi-squared distance over successive overlaping
## intervals of length 4
biofam.chi.ostep <- seqdist(biofam.seq, method = "CHI2",
step = 4, overlap = TRUE)
## =====================
## Example with missings
## =====================
data(ex1)
ex1.seq <- seqdef(ex1[, 1:13])
## OM with substitution costs based on transition
## probabilities and indel set as half the maximum
## substitution cost
costs.tr <- seqcost(ex1.seq, method = "TRATE",
with.missing = TRUE)
ex1.om <- seqdist(ex1.seq, method = "OM",
indel = costs.tr$indel, sm = costs.tr$sm,
with.missing = TRUE)
## Localized OM
ex1.omloc <- seqdist(ex1.seq, method = "OMloc",
indel = costs.tr$indel, sm = costs.tr$sm,
with.missing = TRUE)
## OM of spells
ex1.omspell <- seqdist(ex1.seq, method = "OMspell",
sm = costs.tr$sm, indel = costs.tr$indel,
with.missing = TRUE)
## Distance based on number of matching subsequences
ex1.nms <- seqdist(ex1.seq, method = "NMS",
with.missing = TRUE)
## Using the sequence vetorial representation metric
costs.fut <- seqcost(ex1.seq, method = "FUTURE", lag = 4,
proximities = TRUE, with.missing = TRUE)
ex1.svr <- seqdist(ex1.seq, method = "SVRspell",
prox = costs.fut$prox, with.missing = TRUE)

