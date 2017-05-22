# http://ggplot2.tidyverse.org/reference/labs.html 
library(extrafont)
loadfonts()
pdf('fonttest.pdf')
library(ggplot2)
p <- ggplot(mtcars, aes(mpg, wt, colour = cyl)) + geom_point()
p + labs(colour = "Cylinders")
#p <- ggplot(mtcars, aes(x=wt, y=mpg)) + geom_point()
#p + labs(axis.title.x=theme_text(size=16, family="Purisa", colour="red"))
dev.off()
embed_fonts('fonttest.pdf', outfile='fonttest-embed.pdf')

