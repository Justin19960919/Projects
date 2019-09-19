# https://medium.com/@pblcollect/r語言文字探勘-語意分析applying-on-mooc-實作-9a3e14523998
# https://mropengate.blogspot.com/2016/04/tf-idf-in-r-language.html
# https://github.com/zoey7407/CSX_RProject_Spring_2018/blob/master/hw5/hw5.Rmd

library(SnowballC)
library(plyr)
library(slam)
library(NLP)
library(tm)
library(jiebaRD)
library(jiebaR)
library(RColorBrewer)
library(wordcloud)
library(dplyr)
library(wordcloud2)
library(dplyr)
library(stringr)
install.packages("showtext")
library(showtext)
library(writexl)
# download wordcloud
require(devtools)
install_github("lchiffon/wordcloud2")


## read in file
library(readxl)
opinion_7 <- read_excel("Desktop/opinion_7.xlsx")


#################################### EDA & Regression ################################################


## clean data
opinion_7<-opinion_7[c(colnames(opinion_7)[c(1,2,3,6,10,11,13,16,17,19,20,21,22,23)])]

opinion_7$整體滿意度<-factor(opinion_7$整體滿意度,levels=c(1,2,3))


opinion_7$`Source Type`<-factor(opinion_7$`Source Type`)
opinion_7$餐點風味<-factor(opinion_7$餐點風味,levels=c(1,2,3,4,5))
opinion_7$服務速度<-factor(opinion_7$服務速度,levels=c(1,2,3,4,5))
opinion_7$承諾時間的正確度<-factor(opinion_7$承諾時間的正確度,levels=c(1,2,99))
opinion_7$`餐點正確性 Pizza Hut`<-factor(opinion_7$`餐點正確性 Pizza Hut`,levels=c(1,2))
opinion_7$在消費時遇到問題<-factor(opinion_7$在消費時遇到問題,levels=c(1,2))
opinion_7$感到物超所值<-factor(opinion_7$感到物超所值,levels=c(1,2,3,4,5))
opinion_7$消費類型<-factor(opinion_7$消費類型,levels=c(1,2,4))
opinion_7$`Day of Week`<-factor(opinion_7$`Day of Week`,levels=c(1,2,3,4,5,6,7))


## chi-square tests
chisq.test(table(opinion_7$整體滿意度,opinion_7$餐點風味))# p-value< 2.2e-16
chisq.test(table(opinion_7$整體滿意度,opinion_7$服務速度)) # p-value < 2.2e-16
chisq.test(table(opinion_7$整體滿意度,opinion_7$承諾時間的正確度)) # p-value 3.896e-16
chisq.test(table(opinion_7$整體滿意度,opinion_7$`餐點正確性 Pizza Hut`)) # p-value5.805e-12
chisq.test(table(opinion_7$整體滿意度,opinion_7$在消費時遇到問題))# p-value5.805e-12
chisq.test(table(opinion_7$整體滿意度,opinion_7$感到物超所值))# p-value< 2.2e-16

chisq.test(table(opinion_7$整體滿意度,opinion_7$消費類型))# p-value0.7307
chisq.test(table(opinion_7$整體滿意度,opinion_7$`Day of Week`))# p-value0.8775

## ordinal logistic regression 
install.packages("MASS")
library(MASS)
model_fit<-polr(整體滿意度~餐點風味+服務速度+承諾時間的正確度+`餐點正確性 Pizza Hut`+在消費時遇到問題+感到物超所值,data=opinion_7,Hess = TRUE)
summary(model_fit)

## signifigance of coefficients and intercepts
summary_table <- coef(summary(model_fit))
pval <- pnorm(abs(summary_table[, "t value"]),lower.tail = FALSE)* 2
summary_table <- cbind(summary_table, "p value" = round(pval,3))
summary_table



## checking 客訴
sort(table(opinion_7$單位),decreasing = TRUE)
## n>=10 
# n=26    886P055 - Ta-Shih (DA)
View(opinion_7[opinion_7$單位=="886P055 - Ta-Shih (DA)",])
## 觀察到 這家店的評價都跟該店家很有關

# n=11    886P070 - Chung Ho Gin Hin (GH) 
View(opinion_7[opinion_7$單位=="886P070 - Chung Ho Gin Hin (GH)",])
# n=10    "886P005 - Kuang Fu (KF)","886P014 - Lung Chiang","886P023 - Wan Ta-Delco (WT)","886P062 - Nankang (NK)"
View(opinion_7[opinion_7$單位 %in% c("886P070 - Chung Ho Gin Hin (GH)","886P005 - Kuang Fu (KF)","886P014 - Lung Chiang","886P023 - Wan Ta-Delco (WT)","886P062 - Nankang (NK)"),])


#################################### Text Mining ################################################

## text data
feedback<- data.frame(opinions=opinion_7$用餐經驗不好)

## functions
toSpace <- content_transformer(function(x, pattern) {
  return (gsub(pattern, "", x))
})

## Words to replace
ReplaceWords<-c("我","再","說","給","卻","跟","覺","會","們","都","很","才","的","及","為","是","在","有","得","了","更","要","讓","也","就","與","何","和","但","月","後","所以","如果","可以","可能","嗎")

AddWords <- c(
  "一直",
  "時間",
  "員工",
  "因為",
  "晚到",
  "很慢",
  "太久",  
  "不錯",
  "好吃",
  "難吃",
  "必勝客",
  "達美樂",
  "拿坡里",
  "披薩",
  "pizza",
  "foodpanda",
  "ubereats",
  "冷掉",
  "網購",
  "外送",
  "外帶",
  "取餐",
  "PK",
  "肯德基",
  "芝心腸",
  "夢時代",
  "必省Q",
  "辣椒粉",
  "抵店",
  "門市",
  "口味",
  "付現",
  "刷卡",
  "街口",
  "起司塔",
  "HOT到家",
  "可樂",
  "買大送小",
  "舊金山",
  "買大送小",
  "個人",
  "獨享",
  "鬆厚",
  "芝心",
  "波羅",
  "薄脆",
  "超級總匯",
  "夏威夷",
  "拼盤",
  "章魚燒",
  "QQ球",
  "起司餃",
  "優惠碼",
  "聚餐",
  "熱NOW配",
  "熱鬧配",
  "PBB",
  "歡樂吧",
  "起士",
  "義大利麵",
  "焗烤",
  "cp值"
)


text_preprocess<-function(Content,WordsToReplace){
  
  docs <- Corpus(VectorSource(Content))
  
  ## Replace
  symbols<-c("。","?","!"," ","-"," ")
  for(i in 1:length(symbols)){
    docs<-tm_map(docs,toSpace, symbols[i])
  }
  
  docs <- tm_map(docs,str_to_lower)
  docs <- tm_map(docs, removePunctuation) 
  docs <- tm_map(docs, removeNumbers)
  docs <- tm_map(docs,str_replace,pattern="pizza",replacement="披薩")
  docs <- tm_map(docs,str_replace,pattern="piaaz",replacement="披薩")
  for(i in 1:length(WordsToReplace)){
    docs<-tm_map(docs,toSpace, WordsToReplace[i])
  }
  docs <- tm_map(docs, stripWhitespace)
  docs<-gsub('[[:punct:]]', '', docs)
  
  return(docs)
}

opinions<-as.vector(feedback$opinions)

seg<-lapply(opinions,text_preprocess,WordsToReplace=ReplaceWords)


#### Original jieba tokenizing function
# jieba_tokenizer=function(d){
#   unlist(segment(d[[1]],mixseg))
# }

jieba_tokenizer=function(d){
  unlist(segment(d[1],mixseg))
}


##建立切截與關鍵字
mixseg = worker()
new_user_word(mixseg, AddWords)
seg = lapply(seg, jieba_tokenizer)


## done  每則評論分開了，且斷詞成功

## frequency
freqframe<-as.data.frame(table(unlist(seg)))
freqframe<-freqframe[order(freqframe$Freq,decreasing = TRUE),]
write_xlsx(freqframe, "Desktop/Comment_Frequency.xlsx")



## Do Term document Matrix (TDM)
d.corpus = VCorpus(VectorSource(seg))  ## Vcorpus: get vector out in the corpus; delete "c()"
inspect(d.corpus)
tdm = TermDocumentMatrix(d.corpus, control = list(wordLengths = c(2,Inf)))


## TDM = as.data.frame(as.matrix(tdm))
## View(TDM)
## What words repeatedly appear in comments?
## View((as.data.frame(sort(apply(TDM,1,sum),decreasing = TRUE))))

## tf-idf
tdm.tfidf<-weightTfIdf(tdm, normalize = T) 
dtm<-as.matrix(tdm.tfidf)
v<-sort(rowSums(dtm), decreasing = T) 
d<-data.frame(words=names(v),tf_idf=v)
write_xlsx(d, "Desktop/Comment_TfIdf.xlsx")
#View(d)




## clustering
tfidf_filter<- removeSparseTerms(tdm.tfidf, 0.95) 
tdm_clust = as.TermDocumentMatrix(tfidf_filter) 
tdm_clust <- weightTfIdf(tdm_clust)
tdm_clust <- as.matrix(tdm_clust) 
tdm_clust_scale <- scale(tdm_clust)
distance<- dist(tdm_clust_scale)
fit <- hclust(distance)
par(family="HiraginoSansCNS-W3")
png("Desktop/CommentDendogram.png")
plot(fit,main="Comment Dendogram")
dev.off()

## show chinese words
# https://blog.gtwang.org/r/how-to-use-your-favorite-fonts-in-r-charts/ 
#showtext.auto(enable = TRUE)
#font.add("ST", "/System/Library/Fonts/STHeiti Light.ttc")





