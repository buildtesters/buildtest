library(gamlss.data)
data(aids)
attach(aids)
plot(x,y,pch=21,bg=c("red","green3","blue","yellow")[unclass(qrt)])
detach(aids)

