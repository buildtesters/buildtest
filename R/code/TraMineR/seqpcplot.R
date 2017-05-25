library(TraMineR)
## ================
## plot biofam data
## ================
data(biofam)
lab <- c("Parent","Left","Married","Left+Marr","Child","Left+Child",
"Left+Marr+Child","Divorced")
## plot state sequences in STS representation
## ==========================================
## creating the weighted state sequence object.
biofam.seq <- seqdef(data = biofam[,10:25], labels = lab,
weights = biofam$wp00tbgs)
## select the first 20 weighted sequences (sum of weights = 18)
biofam.seq <- biofam.seq[1:20, ]
par(mar=c(4,8,2,2))
seqpcplot(seqdata = biofam.seq, order.align = "time")
## .. or
seqplot(seqdata = biofam.seq, type = "pc", order.align = "time")
## Distinct successive states (DSS)
## ==========================================
seqplot(seqdata = biofam.seq, type = "pc", order.align = "first")
## .. or (equivalently)
biofam.DSS <- seqdss(seqdata = biofam.seq) # prepare format
seqpcplot(seqdata = biofam.DSS)
## plot event sequences
## ====================
biofam.eseq <- seqecreate(biofam.seq, tevent = "state") # prepare data
## plot the time in the x-axis
seqpcplot(seqdata = biofam.eseq, order.align = "time", alphabet = lab)
## ordering of events
seqpcplot(seqdata = biofam.eseq, order.align = "first", alphabet = lab)
## ... or
plot(biofam.eseq, order.align = "first", alphabet = lab)
## additional arguments
## ====================
## non-embeddable sequences
seqpcplot(seqdata = biofam.eseq, ltype = "non-embeddable",
order.align = "first", alphabet = lab)
## align on last event
par(mar=c(4,8,2,2))
seqpcplot(seqdata = biofam.eseq, order.align = "last", alphabet = lab)
## use group variables
seqpcplot(seqdata = biofam.eseq, group = biofam$sex[1:20],
order.align = "first", alphabet = lab)
## color patterns (Parent)-(Married) and (Parent)-(Left+Marr+Child)
par(mfrow = c(1, 1))
seqpcplot(seqdata = biofam.eseq,
filter = list(type = "sequence",
value=c("(Parent)-(Married)",
"(Parent)-(Left+Marr+Child)")),
alphabet = lab, order.align = "first")
## color subsequence pattern (Parent)-(Left)
seqpcplot(seqdata = biofam.eseq,
filter = list(type = "subsequence",
value = "(Parent)-(Left)"),
alphabet = lab, order.align = "first")
## color sequences over 10% (within group) (function method)
seqpcplot(seqdata = biofam.eseq,
filter = list(type = "function",
value = "minfreq",
level = 0.1),
alphabet = lab, order.align = "first", seed = 1)
## .. same result using the convenience functions
seqpcplot(seqdata = biofam.eseq,
filter = 0.1,
alphabet = lab, order.align = "first", seed = 1)
seqpcplot(seqdata = biofam.eseq,
filter = seqpcfilter("minfreq", 0.1),
alphabet = lab, order.align = "first", seed = 1)
## highlight the 50% most frequent sequences
seqpcplot(seqdata = biofam.eseq,
filter = list(type = "function",
value = "cumfreq",
level = 0.5),
alphabet = lab, order.align = "first", seed = 2)
## .. same result using the convenience functions
seqpcplot(seqdata = biofam.eseq,
filter = seqpcfilter("cumfreq", 0.5),
alphabet = lab, order.align = "first", seed = 2)
## linear gradient
seqpcplot(seqdata = biofam.eseq,
filter = list(type = "function",
value = "linear"),
alphabet = lab, order.align = "first", seed = 2)
seqpcplot(seqdata = biofam.eseq,
filter = seqpcfilter("linear"),
alphabet = lab, order.align = "first", seed = 1)

