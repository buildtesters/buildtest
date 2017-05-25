# https://cran.r-project.org/web/packages/formatR/formatR.pdf
library(formatR)
path = tempdir()
file.copy(system.file("demo", package = "base"), path, recursive = TRUE)
tidy_dir(path, recursive = TRUE)
