#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("At least one argument must be supplied (input file).n", call.=FALSE)
} else if (length(args)==1) {
  # default output file
  args[2] = "out.csv"
}

strsplit(args[1], "/")[[1]][[2]]
thandle <- strsplit(strsplit(args[1], "/")[[1]][[2]], "_(?=[^_]+$)", perl=TRUE)[[1]][[1]]

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
data_set$DateTime <- as.Date(data_set$DateTime) 
x_labels <- pretty(c(min(data_set$DateTime), max(data_set$DateTime)), n=8)

# Sort the CSV files by dates
# data_set[order(data_set$DateTime, decreasing = FALSE)]
# data_set[order(as.Date(data_set$DateTime, format="%d/%m/%Y")),]

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





