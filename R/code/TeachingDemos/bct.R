# https://cran.r-project.org/web/packages/TeachingDemos/TeachingDemos.pdf
library(TeachingDemos)
y <- rlnorm(500, 3, 2)
par(mfrow=c(2,2))
qqnorm(y)
qqnorm(bct(y,1/2))
qqnorm(bct(y,0))
hist(bct(y,0))
