library(gam)
# fit a model with a linear term in Age and a random effect in the factor Level
y ~ Age + random(Level, lambda=1)

