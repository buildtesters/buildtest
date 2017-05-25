library(TraMineR)
## Defining a sequence object with the data in columns 10 to 25
## (family status from age 15 to 30) in the biofam data set
data(biofam)
biofam.lab <- c("Parent", "Left", "Married", "Left+Marr",
"Child", "Left+Child", "Left+Marr+Child", "Divorced")
biofam.seq <- seqdef(biofam, 10:25, labels=biofam.lab)
## Computing the distance matrix
costs <- seqsubm(biofam.seq, method="TRATE")
biofam.om <- seqdist(biofam.seq, method="OM", sm=costs)
## Representative set using the neighborhood density criterion
biofam.rep <- seqrep(biofam.seq, diss=biofam.om, criterion="density")
biofam.rep
summary(biofam.rep)
plot(biofam.rep)
