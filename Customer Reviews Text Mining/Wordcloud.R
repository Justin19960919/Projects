### Pizza Hut July Customer response text mining

## input data
library(readxl)
opinion_7 <- read_excel("~/Downloads/opinion_7.xlsx")

## libraries for text mining
install.packages("rJava")
install.packages("tm")
install.packages("wordcloud")
install.packages("jiebaR")
install.packages("jiebaRD")
install.packages("RColorBrewer")
install.packages("wordcloud")
install.packages("SnowballC")
install.packages("dplyr")

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

# download wordcloud
require(devtools)
install_github("lchiffon/wordcloud2")




## preprocessing
feedback<-opinion_7$用餐經驗不好
docs <- Corpus(VectorSource(feedback))
toSpace <- content_transformer(function(x, pattern) {
  return (gsub(pattern, "", x))
})


## Punctuation to replace
symbols<-c("。","?","!"," ","-"," ")
for(i in 1:length(symbols)){
  docs<-tm_map(docs,toSpace, symbols[i])
}

docs <- tm_map(docs, removePunctuation) 
docs <- tm_map(docs, removeNumbers)

## to lower case
docs<-tm_map(docs,str_to_lower)
docs<-tm_map(docs,str_replace,pattern="pizza",replacement="披薩")




## Words to replace
WordsToReplace<-c("我","再","說","給","卻","跟","覺","會","們","沒","都","很","才","的","及","為","是","在","有","得","了","更","要","讓","也","就","不","與","何","和","但","月","後","所以","如果","可以","可能","嗎")

for(i in 1:length(WordsToReplace)){
  docs<-tm_map(docs,toSpace, WordsToReplace[i])
}


docs <- tm_map(docs, stripWhitespace)
docs<-gsub('[[:punct:]]', '', docs)


#建立切截與關鍵字
mixseg = worker()
keyword <- c(
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
"冷掉",
"網購",
"外送",
"外帶",
"取餐",
"PK雙饗卡",
"PK",
"PK卡",
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
"焗烤"
)

new_user_word(mixseg, keyword)
jieba_tokenizer=function(d){
  unlist(segment(d[[1]],mixseg))
}
seg = lapply(docs, jieba_tokenizer)

##詞頻
freqFrame = as.data.frame(table(unlist(seg)))
freqFrame$Var1<-as.character(freqFrame$Var1)
## sorted and words length>2
sort_words<-freqFrame%>%filter(Freq>10)%>%arrange(desc(Freq))
View(sort_words)


### Wordcloud 
# wordcloud2(data = sort_words,fontWeight = "bold"
#           ,size = 1,color = "random-light",shape='circle')

pal <- brewer.pal(8, 'Dark2')
wordcloud(sort_words$Var1,sort_words$Freq,min.freq = 9,
          random.order=F,random.color=T, 
          rot.per=0.3,colors=pal,
          use.r.layout = F,fixed.asp=T,family='Heiti TC Light')


## Tf-idf 

d.corpus<-Corpus(VectorSource(seg))
tdm <- TermDocumentMatrix(d.corpus)
inspect(tdm)


tokens <- lapply(seg,function(d){as.data.frame(table(d))})
TDM = tokens[[1]]






## Clustering Dendogram ; correlation between words











