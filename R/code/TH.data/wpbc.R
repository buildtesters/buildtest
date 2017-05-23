library(TH.data)
data("wpbc", package = "TH.data")
### fit logistic regression model
coef(glm(status ~ ., data = wpbc[,colnames(wpbc) != "time"],
family = binomial()))
