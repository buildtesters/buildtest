library(testthat)
describe("matrix()", {
it("can be multiplied by a scalar", {
m1 <- matrix(1:4, 2, 2)
m2 <- m1 * 2
expect_equivalent(matrix(1:4 * 2, 2, 2), m2)
})
it("can have not yet tested specs")
})
# Nested specs:
## code
addition <- function(a, b) a + b
division <- function(a, b) a / b
## specs
describe("math library", {
describe("addition()", {
it("can add two numbers", {
expect_equivalent(1 + 1, addition(1, 1))
})
})
describe("division()", {
it("can divide two numbers", {
expect_equivalent(10 / 2, division(10, 2))
})
it("can handle division by 0") #not yet implemented
})
})
