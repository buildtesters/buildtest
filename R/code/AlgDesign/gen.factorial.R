# https://cran.r-project.org/web/packages/AlgDesign/AlgDesign.pdf
library(AlgDesign)
dat<-gen.factorial(3,3)
dat<-gen.factorial(c(3,2,3))
dat<-gen.factorial(3,3,factors="all")
dat<-gen.factorial(3,3,varNames=c("A","B","C"))
