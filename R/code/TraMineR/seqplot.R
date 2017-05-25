library(TraMineR)
## ======================================================
## Creating state sequence objects from example data sets
## ======================================================
## biofam data set
data(biofam)
## We use only a sample of 300 cases
set.seed(10)
biofam <- biofam[sample(nrow(biofam),300),]
biofam.lab <- c("Parent", "Left", "Married", "Left+Marr",
"Child", "Left+Child", "Left+Marr+Child", "Divorced")
biofam.seq <- seqdef(biofam, 10:25, labels=biofam.lab)
## actcal data set
data(actcal)
## We use only a sample of 300 cases
set.seed(1)
actcal <- actcal[sample(nrow(actcal),300),]
actcal.lab <- c("> 37 hours", "19-36 hours", "1-18 hours", "no work")
actcal.seq <- seqdef(actcal,13:24,labels=actcal.lab)
## ex1 using weights
data(ex1)
ex1.seq <- seqdef(ex1, 1:13, weights=ex1$weights)
## ========================
## Sequence frequency plots
## ========================
## Plot of the 10 most frequent sequences
seqplot(biofam.seq, type="f")
## Grouped by sex
seqfplot(actcal.seq, group=actcal$sex)
## Unweighted vs weighted frequencies
seqfplot(ex1.seq, weighted=FALSE)
seqfplot(ex1.seq, weighted=TRUE)
## =====================
## Modal states sequence
## =====================
seqplot(biofam.seq, type="ms")
## same as
seqmsplot(biofam.seq)
## ====================
## Representative plots
## ====================
## Computing a distance matrix
## with OM metric
costs <- seqsubm(biofam.seq, method="TRATE")
biofam.om <- seqdist(biofam.seq, method="OM", sm=costs)
## Plot of the representative sets grouped by sex
## using the default density criterion
seqrplot(biofam.seq, group=biofam$sex, diss=biofam.om)
## Plot of the representative sets grouped by sex
## using the "dist" (centrality) criterion
seqrplot(biofam.seq, group=biofam$sex, criterion="dist", diss=biofam.om)
## ====================
## Sequence index plots
## ====================
## First ten sequences
seqiplot(biofam.seq)
## All sequences sorted by age in 2000
## grouped by sex
## using 'border=NA' and 'space=0' options to have a nicer plot
seqiplot(actcal.seq, group=actcal$sex, idxs=0, border=NA, space=0,
sortv=actcal$age00)
## =======================
## State distribution plot
## =======================
## biofam grouped by sex
seqplot(biofam.seq, type="d", group=actcal$sex)
## actcal grouped by sex
seqplot(actcal.seq, type="d", group=actcal$sex)
## ===================
## Cross-sectional entropy plot
## ===================
seqplot(biofam.seq, type="Ht", group=biofam$sex)
## ===============
## Meant time plot
## ===============
## actcal data set, grouped by sex
seqplot(actcal.seq, type="mt", group=actcal$sex)
## biofam data set, grouped by sex
seqmtplot(biofam.seq, group=biofam$sex)

