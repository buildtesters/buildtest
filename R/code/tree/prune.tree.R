library(tree)
data(fgl, package="MASS")
fgl.tr <- tree(type ~ ., fgl)
plot(print(fgl.tr))
fgl.cv <- cv.tree(fgl.tr,, prune.tree)
for(i in 2:5) fgl.cv$dev <- fgl.cv$dev +
cv.tree(fgl.tr,, prune.tree)$dev
fgl.cv$dev <- fgl.cv$dev/5
plot(fgl.cv)
