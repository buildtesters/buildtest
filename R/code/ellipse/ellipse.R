# https://cran.r-project.org/web/packages/ellipse/ellipse.pdf
library(ellipse)
data(USAccDeaths)
fit <- arima0(USAccDeaths, order = c(0, 1, 1), seasonal = list(order = c(0, 1, 1)))
# Plot the approximate 95% confidence region for the first two parameters
# of the model
plot(ellipse(fit), type = 'l')
points(fit$coef[1], fit$coef[2])

