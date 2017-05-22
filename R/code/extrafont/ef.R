library(extrafont)
library(ggplot2)

my_pdf <- function(file, width, height){
  loadfonts()
  pdf(file = file, width = width, height = height,
      family = "ArialMT")
}

my_pdf("ArialTester.pdf")
g <- qplot(1:10, 1:10, "point") + ggtitle(paste0(LETTERS,letters, collapse="")) +
  theme(text = element_text(family = "Arial"))
plot(g)
dev.off()
embed_fonts("ArialTester.pdf")
