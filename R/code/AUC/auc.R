# https://cran.r-project.org/web/packages/AUC/AUC.pdf
library(AUC)
data(churn)
auc(sensitivity(churn$predictions,churn$labels))
auc(specificity(churn$predictions,churn$labels))
auc(accuracy(churn$predictions,churn$labels))
auc(roc(churn$predictions,churn$labels))

