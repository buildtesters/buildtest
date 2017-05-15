#  https://cran.r-project.org/web/packages/adegenet/adegenet.pdf

library(adegenet)
data(nancycats)
nancycats
pop(nancycats) # get the populations
indNames(nancycats) # get the labels of individuals
locNames(nancycats) # get the labels of the loci
alleles(nancycats) # get the alleles
head(tab(nancycats)) # get allele counts
# get allele frequencies, replace NAs
head(tab(nancycats, freq = TRUE, NA.method = "mean"))
# let's isolate populations 4 and 8
popNames(nancycats)
obj <- nancycats[pop=c(4,8)]
obj
popNames(obj)
pop(obj)
# let's isolate two markers, fca23 and fca90
locNames(nancycats)
obj <- nancycats[loc=c("fca23","fca90")]
obj
locNames(obj)
# illustrate pop
obj <- nancycats[sample(1:100, 10)]
pop(obj)
pop(obj) <- rep(c('b', 'a'), each = 5)
pop(obj)
# illustrate locNames
locNames(obj)
locNames(obj, withAlleles = TRUE)
locNames(obj)[1] <- "newLocus"
locNames(obj)
locNames(obj, withAlleles=TRUE)
# illustrate how 'other' slot is handled
data(sim2pop)
nInd(sim2pop)
other(sim2pop[1:6]) # xy is subsetted automatically
other(sim2pop[1:6, treatOther=FALSE]) # xy is left as is

