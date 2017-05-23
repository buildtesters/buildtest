library(tibble)
has_rownames(mtcars)
has_rownames(iris)
has_rownames(remove_rownames(mtcars))
head(rownames_to_column(mtcars))
mtcars_tbl <- as_tibble(rownames_to_column(mtcars))
mtcars_tbl
column_to_rownames(as.data.frame(mtcars_tbl))

