library(tree)
data(shuttle, package="MASS")
shuttle.tr <- tree(use ~ ., shuttle, subset=1:253,
mindev=1e-6, minsize=2)
shuttle.tr
shuttle1 <- shuttle[254:256, ] # 3 missing cases
predict(shuttle.tr, shuttle1)
