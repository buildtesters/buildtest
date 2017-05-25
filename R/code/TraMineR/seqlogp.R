library(TraMineR)
## Creating the sequence objects using weigths
data(biofam)
biofam.seq <- seqdef(biofam, 10:25, weights=biofam$wp00tbgs)
## Computing sequence probabilities
biofam.prob <- seqlogp(biofam.seq)
## Comparing the probability of each cohort
cohort <- biofam$birthyr>1940
boxplot(biofam.prob~cohort)
