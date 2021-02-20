# Projects
---
### Auto-Exploratory-Data-vis
This is a script that used  R to do auto exploratory data visualization based on the 
data columns data type. The function pairs 2x2 columns, when facing continuous variables
it does a pearson correlation and a linear regression. When facing categorical variables 
and continuous variables, it checks for Gaussian distribution for the continuous variable,
and does either a T-test or a wilcoxon signed rank test. If categorical variables > 2, then
we do a anova or a kruskal wallis test accordingly. This script was written back in 2018.


### Customer Reviews Text Mining
This is a mini text mining project that uses R to text mine customer complaints of pizza 
hut delivery reviews.It outputs a wordcloud and a comment dendogram to get hold of the 
correlation between words, and the importance of words. The dendogram is plotted using
a heirarchial clustering.


