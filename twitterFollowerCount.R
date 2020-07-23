#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "out.csv"
}

strsplit(args[1], "/")[[1]][[3]]
thandle <- strsplit(strsplit(args[1], "/")[[1]][[3]], "_(?=[^_]+$)", perl=TRUE)[[1]][[1]]

f2si2 <- function (number, rounding=F, sep=" ") {
  sign = ""
  if (number < 0){
	number <- number * -1
        sign = "-"
  }
  lut <- c(1e-24, 1e-21, 1e-18, 1e-15, 1e-12, 1e-09, 1e-06, 
      0.001, 1, 1000, 1e+06, 1e+09, 1e+12, 1e+15, 1e+18, 1e+21, 
      1e+24)
  pre <- c("y", "z", "a", "f", "p", "n", "u", "m", "", "k", 
      "M", "B", "T", "P", "E", "Z", "Y")
  ix <- findInterval(number, lut)
  if (ix>0 && lut[ix]!=1) {
    if (rounding==T) {
      sistring <- paste(sign, round(number/lut[ix], 2), pre[ix], sep=sep)
    } else {
      sistring <- paste(sign, round(number/lut[ix], 2), pre[ix], sep=sep)
    }
  } else {
    sistring <- paste(sign, number, sep=sep)
  }
  return(sistring)
}


ifile <- paste(args[1], ".csv", sep="")
data_set <- read.csv(ifile, header=TRUE, as.is=TRUE)

print("CSV File found and loaded")

# Study Range
dates <- as.POSIXct(data_set$DateTime, format="%Y-%m-%d")
data_set$DateTime <- as.Date(data_set$DateTime) 
x_labels <- pretty(c(min(data_set$DateTime), max(data_set$DateTime)), n=8)
options("scipen" = 10)


###
# Follower Count 
###


jpeg(file=paste(thandle,"-follower-count.jpg", sep=""), height=625, width=875)
y_pos <- pretty(data_set$FollowerCount, n=5)
y_pretty <- lapply(y_pos, f2si2, rounding=T, sep="")
titletext <- paste('@', thandle,'\'s Twitter Follower Growth Over Time', sep='')
par(mar=c(5.1, 6.1, 4.1, 2.1))
plot(data_set$DateTime, data_set$FollowerCount, yaxt="n", xaxt="n", ylim=c(min(y_pos), max(y_pos)), xlim=c(min(x_labels), max(x_labels)), type="o", ann=FALSE)
title(main=titletext)
axis(side=2, at=y_pos, labels=y_pretty, las=1)
axis(side=1, at=x_labels, labels=x_labels)
mtext(side=1, text="Date", line=3, cex=1.2)
mtext(side=2, text="Follower Count", line = 4, cex=1.2)

###
# Absolute Relative and Percentage to first memento Follower Count
###

# Code for Relative Follower Growth
jpeg(file=paste(thandle, "-follower-growth.jpg", sep=""), height=625, width=875)
y_pos <- pretty(data_set$AbsRelative, n=5)
y_pretty <- lapply(y_pos, f2si2, rounding=T, sep="")
y_right_pos <- pretty(data_set$PerRelative, n=5)
titletext <- paste('@', thandle,'\'s Absolute and Percentage Follower \n Growth Over Time w.r.t. First Memento', sep='')
par(mar=c(5.1, 6.1, 5.1, 5.1))
plot(data_set$DateTime, data_set$AbsRelative, yaxt="n", xaxt="n", ylim= c(min(y_pos), max(y_pos)), xlim= c(min(x_labels), max(x_labels)), type = "o", ann=FALSE, pch=16)
axis(side=2, at=y_pos, labels=y_pretty, las=1)
mtext(side = 2, text = "Increase in Follower Count", line=4, cex= 1.2)

# Code for Percentage Follower Growth
box()
par(new=TRUE)
y_right_pretty = lapply(y_right_pos, f2si2, rounding=T, sep="")
plot(data_set$DateTime, data_set$PerRelative, yaxt="n", xaxt="n", ylim= c(min(y_right_pos), max(y_right_pos)), xlim= c(min(x_labels), max(x_labels)), type = "o", ann=FALSE, col="blue", pch=15)
title(main=titletext)
axis(side=1, at=x_labels, labels=x_labels)
axis(side=4, at=y_right_pos, labels=y_right_pretty, las=1, col.axis="blue")
mtext(side = 1, text = "Date", line = 3, cex= 1.2)
mtext(side= 4, text = "% Increase in Follower Count", line = 3, cex= 1.2)
legend("topleft",legend=c("Follower Count Increase","Percentage Change"),
  text.col=c("black","blue"),pch=c(16,15),col=c("black","blue"), cex=1.2)


###
# Absolute to Prev. Memento Follower Count
###


jpeg(file=paste(thandle, "-follower-growth-relative.jpg",sep=''), height=625, width=875)
y_pos <- pretty(data_set$AbsPrevRelative, n=5)
y_pretty <- lapply(y_pos, f2si2, rounding=T, sep="")
titletext <- paste('@', thandle,'\'s Increase in Follower Count Over Time w.r.t. Previous Memento', sep='')
par(mar=c(5.1, 6.1, 4.1, 2.1))
plot(data_set$DateTime, data_set$AbsPrevRelative, yaxt="n", xaxt="n", ylim= c(min(y_pos), max(y_pos)), xlim= c(min(x_labels), max(x_labels)), type = "o", ann=FALSE)
title(main=titletext)
axis(side=2, at=y_pos, labels=y_pretty, las=1)
axis(side=1, at=x_labels, labels=x_labels)
mtext(side = 1, text = "Date", line = 2, cex=1.2)
mtext(side = 2, text = "Increase in Follower Count", line = 4, cex=1.2)

###
# Percentage Relative to Prev. Memento Follower Count
###


jpeg(file=paste(thandle, "-follower-perc-growth-relative.jpg",sep=''), height=625, width=875)
y_pos <- pretty(data_set$PerPrevRelative, n=5)
par(mar=c(5.1, 6.1, 4.1, 2.1))
titletext <- paste('@', thandle,'\'s % Change in Follower Count Over Time w.r.t. Previous Memento', sep='')
plot(data_set$DateTime, data_set$PerPrevRelative, yaxt="n", xaxt="n", ylim= c(min(y_pos), max(y_pos)), xlim= c(min(x_labels), max(x_labels)), type = "o", ann=FALSE)
title(main=titletext)
axis(side=2, at=y_pos, labels=y_pos, las=1)
axis(side=1, at=x_labels, labels=x_labels)
mtext(side = 1, text = "Date", line = 3, cex=1.2)
mtext(side = 2, text = "% Change In Follower Count", line = 4, cex=1.2)


data_set$RateRelative <- data_set$RateRelative * 24 * 3600


###
# Rate Relative to first memento Follower Count
###


jpeg(file=paste(thandle, "-follower-rate.jpg", sep=''), height=625, width=875)
y_pos <- pretty(data_set$RateRelative, n=5)
titletext <- paste('@', thandle,'\'s New Followers Increase in Over Time w.r.t First Memento', sep='')
par(mar=c(5.1, 6.1, 4.1, 2.1))
plot(data_set$DateTime, data_set$RateRelative, yaxt="n", xaxt="n", ylim= c(min(y_pos), max(y_pos)), xlim= c(min(x_labels), max(x_labels)), type = "o", ann=FALSE)
title(main=titletext)
axis(side=2, at=y_pos, labels=y_pos, las=1)
axis(side=1, at=x_labels, labels=x_labels)
mtext(side = 1, text = "Date", line = 3, cex=1.2)
mtext(side = 2, text = "Increase of New Followers in a Day", line = 4, cex=1.2)


data_set$RatePrevRelative <- data_set$RatePrevRelative * 24 * 3600


###
# Rate Relative to Prev. Memento Follower Count
###


jpeg(file=paste(thandle, "-follower-rate-relative.jpg", sep=''), height=625, width=875)
y_pos <- pretty(data_set$RatePrevRelative, n=5)
y_pretty <- lapply(y_pos, f2si2, rounding=T, sep="")
titletext <- paste('@', thandle,'\'s New Followers Increase Over Time w.r.t. Previous Memento', sep='')
par(mar=c(5.1, 6.1, 4.1, 2.1))
plot(data_set$DateTime, data_set$RatePrevRelative, yaxt="n", xaxt="n", ylim= c(min(y_pos), max(y_pos)), xlim= c(min(x_labels), max(x_labels)), type = "o", ann=FALSE)
title(main=titletext)
axis(side=2, at=y_pos, labels=y_pretty, las=1)
axis(side=1, at=x_labels, labels=x_labels)
mtext(side = 1, text = "Date", line = 3, cex=1.2)
mtext(side = 2, text = "Increase of New Followers in a Day", line = 4, cex=1.2)
