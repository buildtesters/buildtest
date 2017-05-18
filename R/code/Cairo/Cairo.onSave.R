# https://cran.r-project.org/web/packages/Cairo/Cairo.pdf
library(Cairo)
if (require(png, quietly=TRUE)) {
dev <- Cairo(800, 600, type='raster')
Cairo.onSave(dev, function(dev, page)
.GlobalEnv$png <- writePNG(Cairo.capture(dev))
)
plot(1:10, col=2)
dev.off()
str(png)
}
