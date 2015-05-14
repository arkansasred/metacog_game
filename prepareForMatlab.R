prepareForMatlab<-function(subject){
    library(stringr)
    balanceInfo<-read.csv(str_join(subject, "/Game/generalData.csv"))
    balance<-balanceInfo[1,"Balance"]
    file<-str_join(subject,"/Generalization/generalization.csv")
    dat<-read.csv(file, stringsAsFactors = F)
    for (i in 1:nrow(dat)){
        if (substr(dat$alienType[i],1,1)=="A"){
            dat$alienType[i] = 1
        }
        else if (substr(dat$alienType[i],1,1)=="B"){
            dat$alienType[i] = 0
        }
        if (balance == 1){
            if(dat$response[i]=="s"){
                dat$response[i] = 1
            }
            else if (dat$response[i] == "c"){
                dat$response[i] = 0
            }
        }
        else if(balance == 0){
            if(dat$response[i]=="s"){
                dat$response[i] = 0
            }
            else if (dat$response[i] == "c"){
                dat$response[i] = 1
            }
        }
        
    }

    ofInterest<-dat[,3:5]
    ofInterest<-apply(ofInterest,2,as.integer)
    write.csv(ofInterest, str_join(subject,"/Generalization/responses.csv"), row.names = F)
    
}

prepareAllForMatlab<-function(){
    require(stringr)
    dirs<-list.dirs(recursive = FALSE)
    dirs_of_interest<-dirs[grepl("Subject", dirs)]
    for (i in 1:length(dirs_of_interest)){
        if (file.exists(str_join(dirs_of_interest[i],"/Generalization/responses.csv"))==FALSE){
            prepareForMatlab(dirs_of_interest[i])
        }
    }
}