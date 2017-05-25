# https://cran.r-project.org/web/packages/forecast/forecast.pdf
library(forecast)
fit <- Arima(WWWusage,c(3,1,0))
plot(forecast(fit))
library(fracdiff)
x <- fracdiff.sim( 100, ma=-.4, d=.3)$series
fit <- arfima(x)
plot(forecast(fit,h=30))
