# Twitter Follower Count History via Internet Archives
This is a Python script that collects follower counts from the Internet Archives, given a Twitter username. This script grabs the follower counts by identifying various CSS Selectors that match the follower count element on the historical Twitter pages for almost every major overhaul their page layout has gone through. The program only collects one data point per month.

## Output
A csv file noting the date of the archived twitter page, the follower count for that date, and a link to the memento.

Optional: A line graph displaying the collected data.

The program will print to the console the date it is currently processing 'YYYYMMDDHHMMSS' and the action taken to show it's progress.

The program will assume any previously avaiable csv file of the proper name contains the proper data that FollowerHist.py would generate and will refrain from asking the archive for that date again. Thus if the data is wrong, the program will not fix it.

## Installation and Usage
### Dependencies
* Python 3
* R* (to create graph)
* bs4 
* urllib
* [archivenow](https://github.com/oduwsdl/archivenow)* (push to archive) 
* datetime* (push to archive)

*optional
 
### Usage
```shell	
$ git clone https://github.com/oduwsdl/FollowerCountHistory.git
$ cd FollowerCountHistory
$ python FollowerHist.py [-g] [-p] <twitter-handle-without-@> 
```
To just create the graph from a csv file
```shell	
$ git clone https://github.com/oduwsdl/FollowerCountHistory.git
$ cd FollowerCountHistory
$ Rscript --vanilla follower_count_linechart.R <twitter-handle-without-@> 
```
This will create a new folder with the name: <twitter-handle-without-@> and create two files in this folder.
* A .csv file that contains the data collected with associated timestamps
* A .png file that contains a line chart of the data collected with X axis representing time
The R script is called from within the Python script so no additional action is required. 

### Options

 	python FollowerHist.py [-g] [-p] <twitter-handle-without-@> 
  
	-g	  Create graph.
	-p	  Push to internet archive. Will only push if last memento is not within current month. Need additional dependencies 	datetime and archivenow. 
	
#### Push to a different Archive

If you wish to push to a different archive when using the option [-p] then you must change an option in the source code. 

In FollowerHist.py the line

	archivenow.push("http://twitter.com/" + uname,"ia")

is interacting with archivenow to push to the interent archive. If you wish to push to all archives available through archivenow then you must change the parameter "ia" to "all".

	archivenow.push("http://twitter.com/" + uname,"all")
	
If you wish to push to a single different archive then see the options listed in [archivenow](https://github.com/oduwsdl/archivenow). However, realize that this program will only collect data from the Internet Archive.



