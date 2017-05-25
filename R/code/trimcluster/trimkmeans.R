library(trimcluster)
set.seed(10001)
n1 <-60
n2 <-60
n3 <-70
n0 <-10
nn <- n1+n2+n3+n0
pp <- 2
X <- matrix(rep(0,nn*pp),nrow=nn)
ii <-0
for (i in 1:n1){
ii <-ii+1
X[ii,] <- c(5,-5)+rnorm(2)
}
for (i in 1:n2){
ii <- ii+1
X[ii,] <- c(5,5)+rnorm(2)*0.75
}
for (i in 1:n3){
ii <- ii+1
X[ii,] <- c(-5,-5)+rnorm(2)*0.75
}
for (i in 1:n0){
ii <- ii+1
X[ii,] <- rnorm(2)*8
}
tkm1 <- trimkmeans(X,k=3,trim=0.1,runs=3)
# runs=3 is used to save computing time.
print(tkm1)
plot(tkm1,X)
