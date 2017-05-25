# https://cran.r-project.org/web/packages/caret/caret.pdf
library(caret)
###################
## 2 class example
lvs <- c("normal", "abnormal")
truth <- factor(rep(lvs, times = c(86, 258)),
levels = rev(lvs))
pred <- factor(
c(
rep(lvs, times = c(54, 32)),
rep(lvs, times = c(27, 231))),
levels = rev(lvs))
xtab <- table(pred, truth)
results <- confusionMatrix(xtab)
as.table(results)
as.matrix(results)
as.matrix(results, what = "overall")
as.matrix(results, what = "classes")
###################
## 3 class example
xtab <- confusionMatrix(iris$Species, sample(iris$Species))
as.matrix(xtab)
