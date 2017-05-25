library(tree)
ir.tr <- tree(Species ~., iris)
plot(ir.tr)
text(ir.tr)

