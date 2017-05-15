# https://cran.r-project.org/web/packages/ADGofTest/ADGofTest.pdf
library(ADGofTest)
set.seed( 123 )
x <- runif( 100 )
ad.test( x )$p.value
ad.test( x, pnorm, 0, 1 )$p.value
replicate( ad.test( rnorm( 100 ), pnorm )$p.value, 100 )
