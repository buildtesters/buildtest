library(tibble)
# Works for lists and vectors, too:
set_tidy_names(3:5)
set_tidy_names(list(3, 4, 5))
# Clean data frames are left unchanged:
set_tidy_names(mtcars)
# By default, all rename operations are printed to the console:
tbl <- as_tibble(structure(list(3, 4, 5), class = "data.frame"),
validate = FALSE)
set_tidy_names(tbl)
# Optionally, names can be made syntactic:
tidy_names("a b", syntactic = TRUE)
