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

#Make sure isn't an empty table
if(nrow(data) == 0){
    print("Data file is empty. No graph created.")
}else{

	dates <- as.POSIXct(data$date, format="%Y-%m-%d")
	#min_date <- as.POSIXct('2007-10-01')
	min_date <- as.Date(min(dates))
	max_date <- as.Date(max(dates))
	#min_count <- min(data$count)
	min_count = 0
	max_count <- max(data$count)

	png(paste(uname,'-line.png',sep=''), height=460, width=665)
	mar.default <- c(5,2,4,2) + 0.01

	#determine Y label offset based on number range
	textmargin = c(3, 1, 0)
	labelmarginoffset = c(0, 4, 0, 0)
	labelOffset=3
	if(max_count > 999){

		labelmarginoffset = c(0, 5, 0, 0)
		labelOffset=5
		if(max_count > 999999){

			labelmarginoffset = c(0, 6, 0, 0)
			labelOffset=6
			if(max_count > 999999999){

				labelmarginoffset = c(0, 8, 0, 0)
				labelOffset=8
				if(max_count > 999999999999){
					labelmarginoffset = c(0, 9, 0, 0)
					labelOffset=9
				}
			}
		}
	}
	par(mar = mar.default + labelmarginoffset, mgp = textmargin)

	unixdata <- data.frame(date=as.Date(data$date), count=data$count)

  prettyYaxis <- pretty(c(min_count:max_count),n=10)
  prettyXaxis <- pretty(as.Date(c(min_date,max_date)), n=10)

	plot(unixdata, type="o", ylim=c(min_count,max_count), axes=FALSE, ann=FALSE) #, xlim=c(as.numeric(min_date),as.numeric(max_date))

	box()
	titletext <- paste('@',uname,' Follower Count Over Time', sep='')
	title(main=titletext, font.main=4, xlab="Year", ylab ="")
	mtext('Followers',side=2,line=labelOffset)

  axis.Date(1, at=prettyXaxis, labels=prettyXaxis)
  axis(2, las=1, at=prettyYaxis, labels=format(prettyYaxis,scientific=FALSE) )
	dev.off()

}
