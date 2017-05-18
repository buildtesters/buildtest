# https://cran.r-project.org/web/packages/bitops/bitops.pdf
library(bitops)
stopifnot(
bitFlip(-1) == 0,
bitFlip(0 ) == 2^32 - 1,
bitFlip(0, bitWidth=8) == 255
)
