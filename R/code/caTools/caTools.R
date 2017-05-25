# https://cran.r-project.org/web/packages/caTools/caTools.pdf
library(caTools)
# GIF image read & write
write.gif( volcano, "volcano.gif", col=terrain.colors, flip=TRUE,
scale="always", comment="Maunga Whau Volcano")
y = read.gif("volcano.gif", verbose=TRUE, flip=TRUE)
image(y$image, col=y$col, main=y$comment, asp=1)
# test runmin, runmax and runmed
k=25; n=200;
x = rnorm(n,sd=30) + abs(seq(n)-n/4)
col = c("black", "red", "green", "brown", "blue", "magenta", "cyan")
plot(x, col=col[1], main = "Moving Window Analysis Functions (window size=25)")
lines(runmin (x,k), col=col[2])
lines(runmed (x,k), col=col[3])
lines(runmean(x,k), col=col[4])
lines(runmax (x,k), col=col[5])
legend(0,.9*n, c("data", "runmin", "runmed", "runmean", "runmax"), col=col, lty=1 )
# sum vs. sumexact
x = c(1, 1e20, 1e40, -1e40, -1e20, -1)
a = sum(x); print(a)
b = sumexact(x); print(b)

