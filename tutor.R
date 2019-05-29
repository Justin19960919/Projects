install.packages('rvest')


filter_tutor<-function(grade="國一",address="中山區"){

library("rvest")
library("plyr")
library("dplyr")
tutor<-read_html("http://tutors.tw/case2.htm")
tutor_content<-tutor%>%html_nodes('.ts')%>%html_text()

## strip useless figures \r\n\t

trim <- function (x){
  stock<-gsub("[rt]", "", x)
  stock<- gsub("^\\s+|\\s+$", "", stock)
  return(stock)
}

tutor_data<-c()
for(i in 1:7){
  tutor_data<-cbind(tutor_data,tutor_content[seq(i,length(tutor_content),7)])
}
tutor_data<-apply(tutor_data,2,trim)
tutor_data<-as.matrix(tutor_data)
colnames(tutor_data)<-c("Case","Grade","Subject","Address","Conditions","Pay","Situation")
tutor_data<-as.data.frame(tutor_data)

tutor_data<-tutor_data[which(grepl("台北",tutor_data$Address)==TRUE),]


result<-c()
for(gg in 1:length(grade)){
  for(ad in 1:length(address)){
    search_result<-tutor_data[which( (grepl(grade[gg],tutor_data$Grade)==TRUE)&(grepl(address[ad],tutor_data$Address)==TRUE)),]
    result<-rbind(result,search_result)
    }
  }
View(result)


}

## testing
filter_tutor(grade = c("國一","小","國二","國三"),address=c("中山","大同","松山","中正","大安","信義"))




