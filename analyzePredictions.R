prepareFile<-function(subject){
    require(stringr)
    file<-str_join(subject, "/Game/predictionData.csv")
    predData<-read.csv(file, stringsAsFactors = F)
    Block<-1:9
    predData<-cbind(Block,predData)
    #drop<- c("Subject.1", "Subject", "Balance")
    #predData<-predData[,!(names(predData)%in%drop)]
    #file2<-str_join(subject, "/Game/generalData.csv")
    #genData<-read.csv(file2, stringsAsFactors = F)
    #Balance<-genData$Balance[1]
    #target <- which(names(predData) == 'Block')[1]
    #predData<-cbind(predData[,1:target,drop=F], Balance, predData[,(target+1):length(predData),drop=F])
    write.csv(predData, str_join(subject,'/Game/predictionData.csv'), row.names = F)
}

readFile<-function(subject){
    require(stringr)
    file<-str_join(subject, "/Game/predictionData.csv")
    predData<-read.csv(file, stringsAsFactors = F)
    Subject<-gsub("^.*Subject+\\s", "", subject)
    Subject<-as.integer(Subject)
    predData<-cbind(Subject,predData)
    predData
}

getPredictions<-function(){
    dirs<-list.dirs(recursive = FALSE)
    dirs_of_interest<-dirs[grepl("Subject", dirs)]
    predictions<-data.frame()
    for (i in 1:length(dirs_of_interest)){
        predictions<-rbind(predictions, readFile(dirs_of_interest[i]))
    }
    predictions
}

analyzePredictions<-function(){
    library(dplyr)
    predictions<-getPredictions()
    preds.tbl<-tbl_df(predictions)
    summaryPreds<-preds.tbl%>%
        group_by(Condition, Block)%>%
        summarise_each(funs(mean), -Subject)
    summaryPreds
}