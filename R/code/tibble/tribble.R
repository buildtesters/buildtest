library(tibble)
tribble(
~colA, ~colB,
"a", 1,
"b", 2,
"c", 3
)
# tribble will create a list column if the value in any cell is
# not a scalar
tribble(
~x, ~y,
"a", 1:3,
"b", 4:6
)
