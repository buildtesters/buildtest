# extrafont - https://cran.r-project.org/web/packages/extrafont/extrafont.pdf
## Not run:
library(extrafont)
library(ggplot2)
loadfonts()
pdf('fonttest.pdf')
p <- ggplot(mtcars, aes(x=wt, y=mpg)) + geom_point()
p + labs(axis.title.x=element_text(size=16, family="Purisa", colour="red"))
dev.off()
embed_fonts('fonttest.pdf', outfile='fonttest-embed.pdf')
## End(Not run)

