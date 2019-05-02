## Aspect-Based Sentiment Analysis: Findings from Natural Language
## Code File: asba-visualizations-tureen.R

# Author: Tahmeed Tureen - University of Michigan, Ann Arbor

library(ggplot2)

explore.data <- read.csv(file = "exploration_data/category_freq.csv")[,-1] 


labels <- colnames(explore.data)
train.freq <- as.vector(as.matrix(explore.data[2,]))

train.data <- data.frame(labels, train.freq)
ggplot(train.data, aes(labels, train.freq)) +
    geom_bar(stat = "identity", fill = "sienna2", color = "black", width = 0.75) + 
    ggtitle("Frequency of Aspect Categories (Train Data)") + 
    geom_text(aes(label = train.freq), vjust=1.6, color="white", size = 5) + 
    xlab("Aspect Category") + ylab("Frequency") +
    theme_bw() + theme(axis.title.x = element_text(size = 12),
                       axis.title.y = element_text(size = 12),
                       axis.title = element_text(size = 15),
                       axis.text.x = element_text(size = 12),
                       axis.text.y = element_text(size = 12),
                       plot.title = element_text(hjust = 0.5))


test.freq <- as.vector(as.matrix(explore.data[3,]))
test.data <- data.frame(labels, test.freq)
ggplot(test.data, aes(labels, test.freq)) +
    geom_bar(stat = "identity", fill = "skyblue3", color = "black", width = 0.75) + 
    ggtitle("Frequency of Aspect Categories (Test Data)") + 
    geom_text(aes(label = test.freq), vjust=1.6, color="white", size = 5) + 
    xlab("Aspect Category") + ylab("Frequency") + 
    theme_bw() + theme(axis.title.x = element_text(size = 12),
                       axis.title.y = element_text(size = 12),
                       axis.title = element_text(size = 15),
                       axis.text.x = element_text(size = 12),
                       axis.text.y = element_text(size = 12),
                       plot.title = element_text(hjust = 0.5))
    

## Performance Plots

# ngrams.labels <- c("unigrams", "bigrams", "trigrams")
# NB.cat.class <- c(63.02, 66.61, 67.15)
# SVM.cat.class <- c(78.28, 79.35, 78.82)
# LR.cat.class <- c(72.71, 75.4, 75.4)
# 
# cat.class.data <- data.frame(ngrams.labels, NB.cat.class, SVM.cat.class, LR.cat.class)

methods.labels <- rep(c("NB", "SVM", "LR"), each = 3)
ngrams.labels <- rep(c("1-gram", "2-grams", "3-grams"), 3)
scores <- c(63.02, 66.61, 67.15, 78.28, 79.35, 78.82, 72.71, 75.4, 75.4)

cat.classify.data <- data.frame(methods.labels, ngrams.labels, scores)

ggplot(cat.classify.data, aes(x = ngrams.labels, y = scores, group = methods.labels)) +
    geom_line(aes(color = methods.labels), size = 1) + 
    geom_point(aes(color = methods.labels), size = 1.5) +
    geom_text(aes(label = scores), vjust= -1.0) +
    ggtitle("Accuracy Performance for Aspect-Category Classification") + 
    ylab("Accuracy Performance (%)") + xlab("N-gram Feature") + 
    theme_bw() + theme(axis.title.x = element_text(size = 12),
                      axis.title.y = element_text(size = 12),
                      axis.title = element_text(size = 15),
                      axis.text.x = element_text(size = 12),
                      axis.text.y = element_text(size = 12),
                      plot.title = element_text(hjust = 0.5)) + 
    scale_colour_discrete(name = "Statistical Model", 
                          labels = c("Logistic Regression",
                                     "Naive Bayes", "Support Vector Machine")) +
    theme(legend.text = element_text(size = 13))



# Make one for F1 Score
methods.labels <- rep(c("NB", "SVM", "LR"), each = 3)
ngrams.labels <- rep(c("1-gram", "2-grams", "3-grams"), 3)
scores <- c(82.25, 82.56, 82.76, 88.51, 88.34, 87.87, 86.36, 87.50, 87.29)

cat.classify.data <- data.frame(methods.labels, ngrams.labels, scores)

ggplot(cat.classify.data, aes(x = ngrams.labels, y = scores, group = methods.labels)) +
    geom_line(aes(color = methods.labels), size = 1) + 
    geom_point(aes(color = methods.labels), size = 1.5) + 
    # geom_text(aes(label = scores), vjust= -1.1) +
    ggtitle("Aspect-Category Classification") + 
    ylab("F1 Score (%)") + xlab("N-gram Feature") + ylim(c(81.5,89)) +
    theme_bw() + theme(axis.title.x = element_text(size = 12),
                       axis.title.y = element_text(size = 12),
                       axis.title = element_text(size = 15),
                       axis.text.x = element_text(size = 12),
                       axis.text.y = element_text(size = 12),
                       plot.title = element_text(hjust = 0.5)) + 
    scale_colour_discrete(name = "Statistical Model", 
                          labels = c("Logistic Regression",
                                     "Naive Bayes", "Support Vector Machine")) +
    theme(legend.text = element_text(size = 13))



# Make one for Aspect Polarity Classification
methods.labels <- rep(c("NB", "SVM", "LR"), each = 3)
ngrams.labels <- rep(c("1-gram", "2-grams", "3-grams"), 3)
scores <- c(65.53, 68.76, 68.76, 72.89, 71.63, 71.45, 68.4, 71.81, 71.45)

cat.classify.data <- data.frame(methods.labels, ngrams.labels, scores)


ggplot(cat.classify.data, aes(x = ngrams.labels, y = scores, group = methods.labels)) +
    geom_line(aes(color = methods.labels), size = 1) + 
    geom_point(aes(color = methods.labels), size = 1.5) + 
    #geom_text(aes(label = scores), vjust= -0.5) +
    ggtitle("Aspect-Term Sentiment Classification") + 
    ylab("Accuracy (%)") + xlab("N-gram Feature") + ylim(c(60,74)) +
    theme_bw() + theme(axis.title.x = element_text(size = 12),
                       axis.title.y = element_text(size = 12),
                       axis.title = element_text(size = 15),
                       axis.text.x = element_text(size = 12),
                       axis.text.y = element_text(size = 12),
                       plot.title = element_text(hjust = 0.5)) + 
    scale_colour_discrete(name = "Statistical Model", 
                          labels = c("Logistic Regression",
                                     "Naive Bayes", "Support Vector Machine")) +
    theme(legend.text = element_text(size = 13))


# Make one for Category Polarity Classification
methods.labels <- rep(c("NB", "SVM", "LR"), each = 3)
ngrams.labels <- rep(c("1-gram", "2-grams", "3-grams"), 3)
scores <- c(64.99, 67.86, 67.15, 65.17, 66.97, 66.79, 64.27, 66.97, 66.07)

cat.classify.data <- data.frame(methods.labels, ngrams.labels, scores)

ggplot(cat.classify.data, aes(x = ngrams.labels, y = scores, group = methods.labels)) +
    geom_line(aes(color = methods.labels), size = 1) + 
    geom_point(aes(color = methods.labels), size = 1.5) + 
    #geom_text(aes(label = scores), vjust= 1.50) +
    ggtitle("Aspect-Category Sentiment Classification") + 
    ylab("Accuracy (%)") + xlab("N-gram Feature") + ylim(c(63,70)) +
    theme_bw() + theme(axis.title.x = element_text(size = 12),
                       axis.title.y = element_text(size = 12),
                       axis.title = element_text(size = 15),
                       axis.text.x = element_text(size = 12),
                       axis.text.y = element_text(size = 12),
                       plot.title = element_text(hjust = 0.5)) + 
    scale_colour_discrete(name = "Statistical Model", 
                          labels = c("Logistic Regression",
                                     "Naive Bayes", "Support Vector Machine")) +
    theme(legend.text = element_text(size = 13))
