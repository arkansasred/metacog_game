analyzeGeneralization<-function(subject, balance){
    require(stringr)
    unSeenAliens<-c("A04", "A10", "A11", "A12", "B08", "B09", "B11", "B12")
    file <- str_join(subject,"/Generalization/generalization.csv")
    subjData<-read.csv(file, stringsAsFactors = F)
    info<-read.csv(str_join(subject, "/Game/generalData.csv"))
    balance<-info[1,"Balance"]
    condition<-info[1, "Condition"]
    ratings<-vector()
    response<-vector()
    getAccur<-function(alien,response){
        if (balance == 0){
            if((substr(alien,1,1)=='A' & response == 'c') | (substr(alien,1,1)=='B' & response=='s')){
                1
            }
            else{0}
        }
        else if (balance == 1){
            if((substr(alien,1,1)=='A' & response == 's') | (substr(alien,1,1)=='B' & response=='c')){
                1
            }
            else{0}
        }
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
    Subject<-gsub("^.*Subject+\\s", "", subject)
    Subject<-as.integer(Subject)
    accs<-data.frame(Subject,condition,overallAcc,generalizationAcc, phi)
    accs
}

readAll<-function(){
    require(stringr)
    require(dplyr)
    dirs<-list.dirs(recursive = FALSE)
    dirs_of_interest<-dirs[grepl("Subject", dirs)]
    accuracies<-data.frame()
    for (i in 1:length(dirs_of_interest)){
        accuracies<-rbind(accuracies, analyzeGeneralization(dirs_of_interest[i]))
    }
    names(accuracies)<-c("Subject", "Condition", "Overall", "Gen", "Phi")
    accuracies<-accuracies[do.call(order,accuracies),]
    accuracies
    #accuracies.tbl<-tbl_df(accuracies)
    #summary<-accuracies.tbl%>%
     #group_by(Condition)%>%
      #  summarise_each(funs(mean), -Subject)
    #summary
}