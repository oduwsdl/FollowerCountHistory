#!/usr/bin/env Rscript
# Rscript follower_count_linechart.R uname
args <- commandArgs(TRUE)
mround <- function(number, multiple){ multiple * round(number/multiple) }
wd <- function(directory)
setwd(file.path(getwd(), directory))
uname <- args[1]
setwd(paste(getwd(),'/',uname, sep = ''))
datafile <- paste(uname,'.csv', sep='')
today = as.POSIXct(Sys.Date())
twitterbegin <- as.POSIXct('2006-07-15')
data <- read.csv(datafile)
data <- data[order(as.Date(data$date, format="%Y-%m-%d")),]
dates <- as.POSIXct(data$date, format="%Y-%m-%d")
#dates = as.character(data$date)
#min_date <- as.POSIXct('2007-10-01')
min_date <- min(dates)
max_date <- max(dates)
#min_count <- min(data$count)
min_count = 0
max_count <- max(data$count)
png(paste(uname,'-line.png',sep=''), height=460, width=665)
mar.default <- c(5,2,4,2) + 0.01

#determine Y label offset based on number range
textmargin = c(3, 1, 0)
labelmarginoffset = c(0, 4, 0, 0)
if(max_count > 999){
	textmargin = c(5, 1, 0)
	labelmarginoffset = c(0, 5, 0, 0)
	if(max_count > 999999){
		textmargin = c(6, 1, 0)
		labelmarginoffset = c(0, 6, 0, 0)
		if(max_count > 999999999){
			textmargin = c(8, 1, 0)
			labelmarginoffset = c(0, 8, 0, 0)
			if(max_count > 999999999999){
			textmargin = c(10, 1, 0)
			labelmarginoffset = c(0, 10, 0, 0)
		}
		}
	}
} 
par(mar = mar.default + labelmarginoffset,mgp = textmargin) 

unixdata <- data.frame(date=as.numeric(as.POSIXct(data$date)), count=data$count)
plot(unixdata, type="o", col="red", ylim=c(min_count,max_count), xlim=c(min_date,today), axes=FALSE, ann=FALSE) #, xlim=c(as.numeric(min_date),as.numeric(max_date))
box()
titletext <- paste(uname,' Follower Count over Time', sep='')
title(main=titletext, col.main="red", font.main=4, xlab="Year", ylab ="Followers")
axis(1, las=1, at=seq(min_date, today, "12 mon"), labels = format(seq(min_date, today, "12 mon"), "%Y"))
axis(2, las=1, at=seq(0,max_count+(signif(max_count/15,2)-1),mround(signif(max_count/15,2),5)), labels=prettyNum(seq(0,max_count+(signif(max_count/15,2)-1),mround(signif(max_count/15,2),5)),big.mark=",",scientific=FALSE))
dev.off()
