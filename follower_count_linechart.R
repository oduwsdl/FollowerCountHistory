#!/usr/bin/env Rscript
# Rscript follower_count_linechart.R uname
args <- commandArgs(TRUE)
wd <- '~/Desktop/FollowerCountHistory/'
uname <- args[1]
setwd(paste(wd,uname, sep = ''))
datafile <- paste(uname,'.csv', sep='')
today = as.POSIXct(Sys.Date())
twitterbegin <- as.POSIXct('2006-07-15')
data <- read.csv(datafile)
dates <- as.POSIXct(data$date, format="%Y-%m-%d")
#dates = as.character(data$date)
min_date <- as.POSIXct('2006-07-15')
max_date <- max(dates)
min_count <- min(data$count)
max_count <- max(data$count)
png(paste(uname,'-line.png',sep=''), height=460, width=665)
mar.default <- c(5,2,4,2) + 0.01
par(mar = mar.default + c(0, 4, 0, 0)) 
unixdata <- data.frame(date=as.numeric(as.POSIXct(data$date)), count=data$count)
plot(unixdata, type="o", col="red", ylim=c(min_count,max_count), xlim=c(twitterbegin,today), axes=FALSE, ann=FALSE) #, xlim=c(as.numeric(min_date),as.numeric(max_date))
box()
titletext <- paste(uname,' Follower Count over Time', sep='')
title(main=titletext, col.main="red", font.main=4)
axis(1, las=1, at=seq(twitterbegin, today, "12 mon"), labels = format(seq(twitterbegin, today, "12 mon"), "%Y"))
axis(2, las=1, at=seq(0,max_count+(signif(max_count/15,2)-1),signif(max_count/15,2)), labels=prettyNum(seq(0,max_count+(signif(max_count/15,2)-1),signif(max_count/15,2)),big.mark=",",scientific=FALSE))
dev.off()
