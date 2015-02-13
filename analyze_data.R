main<-function(){
    subjects<-c("Subject 1B", "Subject 2B", "Subject 3B", "Subject 4B", "Subject 5B");
    conditions<-c(1,1,2,2,2,2,1,1,1,1)
    readPredictionsPre<-function(subjectDir){
        scorePrediction<-read.table(paste(subjectDir,"/PreTest/scorePrediction.txt", sep=""), col.names = "scorePredPre")
        numPrediction<-read.table(paste(subjectDir,"/PreTest/numberPrediction.txt", sep=""), col.names = "numPredPre")
        predictionsPre<-cbind(scorePrediction,numPrediction)
        predictionsPre
    }
    readActualsPre<-function(subjectDir){
        scoreActual<-read.table(paste(subjectDir,"/PreTest/scoreActual.txt", sep=""), col.names = "scoreActualPre")
        numActual<-read.table(paste(subjectDir,"/PreTest/numberActual.txt", sep=""), col.names = "numActualPre")
        actualsPre<-cbind(scoreActual,numActual)
        actualsPre
    }
    readPredictionsPost<-function(subjectDir){
        scorePrediction<-read.table(paste(subjectDir,"/PostTest/scorePrediction.txt", sep=""), col.names = "scorePredPost")
        numPrediction<-read.table(paste(subjectDir,"/PostTest/numberPrediction.txt", sep=""), col.names = "numPredPost")
        predictionsPost<-cbind(scorePrediction,numPrediction)
        predictionsPost
    }
    readActualsPost<-function(subjectDir){
        scoreActual<-read.table(paste(subjectDir,"/PostTest/scoreActual.txt", sep=""), col.names = "scoreActualPost")
        numActual<-read.table(paste(subjectDir,"/PostTest/numberActual.txt", sep=""), col.names = "numActualPost")
        actualsPost<-cbind(scoreActual,numActual)
        actualsPost
    }
    
    readSubject<-function(subject){
        predictsPre<-readPredictionsPre(subject)
        actualsPre<-readActualsPre(subject)
        predictsPost<-readPredictionsPost(subject)
        actualsPost<-readActualsPost(subject)
        subjectName<-subject
        subject<-cbind(subjectName,predictsPre,predictsPost,actualsPre,actualsPost)
    }
    
    subjectData<-data.frame()
    for (i in 1:length(subjects)){
        subjectData<-rbind(subjectData,readSubject(subjects[i]))
    }
    
    subjectData<-cbind(conditions,subjectData)
    
    library(dplyr);
    
    subjectData_tbl<-tbl_df(subjectData)
    subjectData_tbl<-subjectData_tbl%>%
        group_by(conditions)%>%
        mutate(changeInScore = scoreActualPost-scoreActualPre, changeInNumber = numActualPost-numActualPre)%>%
        mutate(predictionAccuracyChange = abs(numPredPost-numActualPost) - abs(numPredPre-numActualPre))
}