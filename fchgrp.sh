#!/bin/bash
#Basic script for running fch program over multiple users
function printHelp
{
	echo "Usage: ./fchgroup.sh (path_to_txt) (parameter 1) ... (parameter n)"
	echo "fchgrp uses the same parameters as fch:"
	echo "-h                show this help message and exit"
	echo "--st=[DATETIME]   Memento start datetime (in RFC 1123 datetime format)"
	echo "--et=[DATETIME]   Memento end datetime (in RFC 1123 datetime format)"
	echo "--freq=[SECONDS]  Sampling frequency of mementos (in seconds)"
	echo "-f=[PATH]         Output file dump path (DEFAULT: ./fchoutput)"
	exit
}

if [ -z "$1" ]
	then
		echo "Usage: ./fchgrp.sh (path_to_txt) (parameter 1) ... (parameter n)"
		exit
elif [ $1 == "-h" ]
	then 
		printHelp
else
	input=$1
fi	

#shift the parameter list by one to ignore the file name
shift

path="-f="$(pwd)
for var in "$@"
do
	case $var in
		
	--st=*)
		st=$var
		;;
	--et=*)
		et=$var
		;;
	--freq=*)
		freq=$var
		;;
	-f=*)
		path=$var
		;;
	*)
		echo "error: '$var' Unknown Parameter."
		printHelp
		;;
	esac
done

while IFS= read -r user; do
	echo $user
	#Gather Memento data from twitter
	csvpath=$path/$user/$user.csv

	#Create Directory for user data if none exists
	if [ -d ${path#*-f=}/$user ]; then
		#do nothing
		:
	else
		mkdir ${path#*-f=}/$user
	fi

	fch $user $csvpath $st $et $freq

	if [ -f ${csvpath#*-f=} ]; then
		#Generate Graphs from csv data
		Rscript twitterFollowerCount.R ${csvpath#*-f=}
	else
		echo "error: csv file was not created."
	fi

done < $input
