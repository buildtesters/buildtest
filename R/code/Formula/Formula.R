# https://cran.r-project.org/web/packages/Formula/Formula.pdf
library(Formula)
## create a simple Formula with one response and two regressor parts
f1 <- y ~ x1 + x2 | z1 + z2 + z3
F1 <- Formula(f1)
class(F1)
length(F1)
## switch back to original formula
formula(F1)
## create formula with various transformations
formula(F1, rhs = 1)
formula(F1, collapse = TRUE)
formula(F1, lhs = 0, rhs = 2)
## put it together from its parts
as.Formula(y ~ x1 + x2, ~ z1 + z2 + z3)
## update the formula
update(F1, . ~ . + I(x1^2) | . - z2 - z3)
update(F1, . | y2 + y3 ~ .)
# create a multi-response multi-part formula
f2 <- y1 | y2 + y3 ~ x1 + I(x2^2) | 0 + log(x1) | x3 / x4
F2 <- Formula(f2)
length(F2)
## obtain various subsets using standard indexing
## no lhs, first/seconde rhs
formula(F2, lhs = 0, rhs = 1:2)
formula(F2, lhs = 0, rhs = -3)
formula(F2, lhs = 0, rhs = c(TRUE, TRUE, FALSE))
## first lhs, third rhs
formula(F2, lhs = c(TRUE, FALSE), rhs = 3)
