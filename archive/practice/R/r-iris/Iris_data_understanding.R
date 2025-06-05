# Exploratory Data Analysis with R

######################
# Iris dataset
######################

iris <- read.table("iris.csv", header = TRUE, sep = ",")

# View the data

View(iris)

dim(iris)

head(iris)
tail(iris)

colnames(iris)

# Deal with variables types

str(iris)

iris$Species <- as.factor(iris$Species)

str(iris)

levels(iris$Species)

is.numeric(iris$Sepal.Length)

class(iris$Sepal.Length)

# Missing data

sum(is.na(iris))

iris[rowSums(is.na(iris)) > 0, ]

# Data Manipulation

iris_setosa <- iris$Species[iris$Species == 'setosa']
iris_versicolor <- iris$Species[iris$Species == 'versicolor']
iris_virginica <- iris$Species[iris$Species == 'virginica']

length(iris_setosa)
length(iris_versicolor)
length(iris_virginica)

############################
# Display summary statistics
############################

# Position indexes

mean(iris$Sepal.Length)

median(iris$Sepal.Length)

quantile(iris$Sepal.Length, probs = c(0.1, 0.25, 0.75, 0.9))

# Dispersion indexes

var(iris$Sepal.Length)

sd(iris$Sepal.Length)

# Summary statistics

summary(iris)

# Covariance and Correlation

cov(iris$Sepal.Length, iris$Sepal.Width)

cor(iris$Sepal.Length, iris$Sepal.Width)

####################
# Data visualization
####################

# Histogram

hist(iris$Sepal.Length)
hist(iris$Sepal.Width)
hist(iris$Petal.Length)
hist(iris$Petal.Width)

# Empirical cumulative distribution function

ecdf(iris$Sepal.Length)
plot(ecdf(iris$Sepal.Length))

ecdf(iris$Sepal.Width)
plot(ecdf(iris$Sepal.Width), col = "red")

plot(ecdf(iris$Sepal.Length), do.points = FALSE, col = "blue")
plot(ecdf(iris$Sepal.Width), col = "red", add = TRUE)

# Boxplots

boxplot.stats(iris$Sepal.Length)

boxplot(iris$Sepal.Length)

# Scatter plot

plot(iris$Sepal.Length, iris$Sepal.Width, xlab = "Length", ylab = "Width")
