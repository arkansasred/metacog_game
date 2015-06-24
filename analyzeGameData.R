readData<-function(subject){
    require(stringr)
    file<-str_join(subject, "/Game/generalData.csv")
    genData<-read.csv(file, stringsAsFactors = F)
    Subject<-gsub("^.*Subject+\\s", "", subject)
    Subject<-as.integer(Subject)
    genData<-cbind(Subject,genData[,2:length(genData)])
    genData
}