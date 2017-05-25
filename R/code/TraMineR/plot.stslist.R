library(TraMineR)
## Defining a sequence object with the data in columns 10 to 25
## (family status from age 15 to 30) in the biofam data set
data(biofam)
biofam.lab <- c("Parent", "Left", "Married", "Left+Marr",
"Child", "Left+Child", "Left+Marr+Child", "Divorced")
biofam.seq <- seqdef(biofam, 10:25, labels=biofam.lab)
## Plot of the 10 most frequent sequences
## with bar width proportional to the frequency
plot(biofam.seq)
## Plotting the all data set
## with no borders
plot(biofam.seq, idxs=0, space=0, border=NA)
## =======
## Weights
## =======
data(ex1)
ex1.seq <- seqdef(ex1, 1:13, weights=ex1$weights)
plot(ex1.seq)
plot(ex1.seq, weighted=FALSE)

