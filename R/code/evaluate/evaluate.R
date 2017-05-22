# https://cran.r-project.org/web/packages/evaluate/evaluate.pdf
library(evaluate)
samples <- system.file("tests", "testthat", package = "evaluate")
if (file_test("-d", samples)) {
replay(evaluate(file(file.path(samples, "order.r"))))
replay(evaluate(file(file.path(samples, "plot.r"))))
replay(evaluate(file(file.path(samples, "data.r"))))
}
