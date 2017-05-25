library(TH.data)
## Not run:
library("Biobase")
data("Westbc", package = "TH.data")
westbc <- new("ExpressionSet",
phenoData = new("AnnotatedDataFrame", data = Westbc$pheno),
assayData = assayDataNew(exprs = Westbc$assay))
## End(Not run)
