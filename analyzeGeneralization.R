analyzeGeneralization<-function(file){
    unSeenAliens<-c("A04", "A06", "A10", "A12", "B08", "B09", "B11", "B12")
    subjData<-read.table(file,sep=",", col.names = c("alienType","response", "confidenceRating", "RT"))
    subjData$alienType<-as.character(subjData$alienType)
    getAccur<-function(alien,response){
        if((substr(alien,1,1)=='A' & response == 'return') | (substr(alien,1,1)=='B' & response=='space')){
            1
        }
        else{0}
    }
    codeConf<-function(rating){
        if(rating>3){
            1
        }
        else{0}
    }
    accuracies<-vector()
    codedConfs<-vector()
    for (i in 1:nrow(subjData)){
        acc<-getAccur(subjData$alienType[i], subjData$response[i])
        conf<-codeConf(subjData$confidenceRating[i])
        accuracies<-c(accuracies,acc)
        codedConfs<-c(codedConfs, conf)
    }
    subjData<-cbind(subjData,accuracies, codedConfs)
    unSeen<-subjData[subjData$alienType%in%unSeenAliens,]
    overallAcc<-sum(accuracies)/length(accuracies)
    generalizationAcc<-sum(unSeen$accuracies)/length(unSeen$accuracies)
    phi<-cor(subjData$confidenceRating, subjData$accuracies, method = "pearson")
    accs<-c(overallAcc,generalizationAcc, phi)
    accs
}