prepareFile<-function(subject){
    require(stringr)
    file<-str_c(subject, "/Game/predictionData.csv")
    predData<-read.csv(file, stringsAsFactors = F)
    drop<- "X"
    predData<-predData[,!(names(predData)%in%drop)]
    file2<-str_c(subject, "/Game/generalData.csv")
    genData<-read.csv(file2, stringsAsFactors = F)
    Balance<-genData$Balance[1]
    target <- which(names(predData) == 'Block')[1]
    predData<-cbind(Balance, predData)
    write.csv(predData, str_c(subject,'/Game/predictionData.csv'), row.names = F)
}

readFile<-function(subject){
    require(stringr)
    file<-str_c(subject, "/Game/predictionData.csv")
    predData<-read.csv(file, stringsAsFactors = F)
    drop<- "X"
    predData<-predData[,!(names(predData)%in%drop)]
    Subject<-gsub("^.*Subject+\\s", "", subject)
    Subject<-as.integer(Subject)
    predData<-cbind(Subject,predData)
    predData
}

getPredictions<-function(){
    library(dplyr)
    dirs<-list.dirs(recursive = FALSE)
    dirs_of_interest<-dirs[grepl("Subject", dirs)]
    predictions<-data.frame()
    for (i in 1:length(dirs_of_interest)){
        predictions<-rbind(predictions, readFile(dirs_of_interest[i]))
    }
    predictions.tbl<-tbl_df(predictions)
    corrNumber<-predictions.tbl%>%
        select(Subject, Condition, NumberPrediction, NumberActual)%>%
        group_by(Subject, Condition)%>%
        summarize(corrNumber = cor(NumberPrediction, NumberActual, method = "spearman"))
    predictions<-list(predictions, corrNumber)
    predictions
}

analyzePredictions<-function(){
    library(dplyr)
    library(ggplot2)
    library(Rmisc)
    predictions<-getPredictions()
    preds<-predictions[[1]]
    mse<-summarySE(preds, measurevar = "NumberActual", groupvars = c("Condition", "Block"))
    ggplot(mse, aes(x = Block, y = NumberActual, color = factor(Condition))) + geom_point(alpha = 1) + geom_smooth(method = lm)
    preds.tbl<-tbl_df(preds)
    summaryPreds<-preds.tbl%>%
        group_by(Condition, Block)%>%
        summarise_each(funs(sd), -Subject)
    summaryPreds
}