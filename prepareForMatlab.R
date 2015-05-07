prepareForMatlab<-function(subject, balance){
    library(stringr)
    file<-str_join("Subject ",subject,"/Generalization/generalization.csv")
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
    write.csv(ofInterest, str_join("Subject ",subject,"/Generalization/responses.csv"), row.names = F)
    
}