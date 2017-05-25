library(TraMineR)
## Defining a state sequence object
data(mvad)
mvad.seq <- seqdef(mvad[, 17:86])
## Building dissimilarities (any dissimilarity measure can be used)
mvad.ham <- seqdist(mvad.seq, method="HAM")
## Compute distance to center according to group gcse5eq
dc <- disscenter(mvad.ham, group=mvad$gcse5eq)
## Ploting distribution of dissimilarity to center
boxplot(dc~mvad$gcse5eq, col="cyan")
## Retrieving index of the first medoids, one per group
dc <- disscenter(mvad.ham, group=mvad$Grammar, medoids.index="first")
print(dc)
## Retrieving index of all medoids in each group
dc <- disscenter(mvad.ham, group=mvad$Grammar, medoids.index="all")
print(dc)
