analyzePredictions<-function(subject){
    require(stringr)
    file<-str_join(subject, "/Game/predictionData.csv")
    predData<-read.csv(file, stringsAsFactors = F)
    numberDiff<-abs(predData$NumberPrediction-predData$NumberActual)
    scoreCor<-cor(predData$ScorePrediction, predData$ScoreActual)
    list(predData, numberDiff, scoreCor)
}

getPredictions<-function(){
    dirs<-list.dirs(recursive = FALSE)
    dirs_of_interest<-dirs[grepl("Subject", dirs)]
    predictions<-data.frame()
    for (i in 1:length(dirs_of_interest)){
        predictions<-rbind(predictions, analyzePredictions(dirs_of_interest[i]))
    }
    predictions
}