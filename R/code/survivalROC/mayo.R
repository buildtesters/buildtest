# https://cran.r-project.org/web/packages/survivalROC/survivalROC.pdf
library(survivalROC)
data(mayo)
nobs <- NROW(mayo)
cutoff <- 365
## MAYOSCORE 4, METHOD = NNE
Mayo4.1= survivalROC(Stime=mayo$time,
status=mayo$censor,
marker = mayo$mayoscore4,
predict.time = cutoff,span = 0.25*nobs^(-0.20) )
plot(Mayo4.1$FP, Mayo4.1$TP, type="l", xlim=c(0,1), ylim=c(0,1),
xlab=paste( "FP", "\n", "AUC = ",round(Mayo4.1$AUC,3)),
ylab="TP",main="Mayoscore 4, Method = NNE \n Year = 1")
abline(0,1)
## MAYOSCORE 4, METHOD = KM
Mayo4.2= survivalROC(Stime=mayo$time,
status=mayo$censor,
marker = mayo$mayoscore4,
predict.time = cutoff, method="KM")
plot(Mayo4.2$FP, Mayo4.2$TP, type="l", xlim=c(0,1), ylim=c(0,1),
xlab=paste( "FP", "\n", "AUC = ",round(Mayo4.2$AUC,3)),
ylab="TP",main="Mayoscore 4, Method = KM \n Year = 1")
abline(0,1)

