# https://stat.ethz.ch/R-manual/R-devel/library/base/html/MathFun.html
require(stats) # for spline
require(graphics)
xx <- -9:9
plot(xx, sqrt(abs(xx)),  col = "red")
lines(spline(xx, sqrt(abs(xx)), n=101), col = "pink")
