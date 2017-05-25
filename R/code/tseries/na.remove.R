library(tseries)
x<-ts(c(5453.08,5409.24,5315.57,5270.53, # one and a half week stock index
5211.66,NA,NA,5160.80,5172.37)) # data including a weekend
na.remove(x) # eliminate weekend and introduce ``business'' time scale

