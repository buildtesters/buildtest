library(tripack)
# we will use the simple test data from TRIPACK:
data(tritest)
tritest.tr<-tri.mesh(tritest)
opar<-par(mfrow=c(2,2))
plot(tritest.tr)
# include all points in a big triangle:
tritest.tr<-add.constraint(tritest.tr,c(-0.1,2,-0.1),
c(-3,0.5,3),reverse=TRUE)
# insert a small cube:
tritest.tr <- add.constraint(tritest.tr, c(0.4, 0.4,0.6, 0.6),
c(0.6, 0.4,0.4, 0.6),
reverse = FALSE)
par(opar)
