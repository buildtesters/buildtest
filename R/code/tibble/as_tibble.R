library(tibble)
l <- list(x = 1:500, y = runif(500), z = 500:1)
df <- as_tibble(l)
m <- matrix(rnorm(50), ncol = 5)
colnames(m) <- c("a", "b", "c", "d", "e")
df <- as_tibble(m)
# as_tibble is considerably simpler than as.data.frame
# making it more suitable for use when you have things that are
# lists
## Not run:
if (requireNamespace("microbenchmark", quiet = TRUE)) {
  l2 <- replicate(26, sample(letters), simplify = FALSE)
  names(l2) <- letters
  microbenchmark::microbenchmark(
    as_tibble(l2, validate = FALSE),
    as_tibble(l2),
    as.data.frame(l2)
  )
}
if (requireNamespace("microbenchmark", quiet = TRUE)) {
  m <- matrix(runif(26 * 100), ncol = 26)
  colnames(m) <- letters
  microbenchmark::microbenchmark(
    as_tibble(m),
    as.data.frame(m)
  )
}
## End(Not run)

