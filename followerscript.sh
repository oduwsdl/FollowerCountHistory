#!/bin/bash
echo "First Arg: $1"
./main.py --st=20200101000000 --et=20200331000000 --frequency=2592000  --debug $1
Rscript twitterFollowerCount.R "/tmp/$1_analysis"
