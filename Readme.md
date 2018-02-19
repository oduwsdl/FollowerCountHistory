# Twitter Follower Count History via Internet Archives
This is a Python script that collects follower counts from the Internet Archives, given a Twitter username. This script grabs the follower counts by identifying various CSS Selectors that match the follower count element on the historical Twitter pages for almost every major overhaul their page layout has gone through.

## Installation and Usage
Make sure you have Python and R installed on your computer. 
```shell	
$ git clone https://github.com/okrand/FollowerCountHistory.git
$ cd FollowerCountHistory
$ python main.py [-g create graph] [-p push to internet archive] <twitter-handle-without-@> 
```

Options

-g	Create graph.
-p	Push to internet archive. Will only push if last memento is not within current month. Need additional dependencies datetime and archivenow.

To just create the graph from a csv file
```shell	
$ git clone https://github.com/okrand/FollowerCountHistory.git
$ cd FollowerCountHistory
$ Rscript --vanilla follower_count_linechart.R <twitter-handle-without-@> 
```
This will create a new folder with the name: <twitter-handle-without-@> and create two files in this folder.
* A .csv file that contains the data collected with associated timestamps
* A .png file that contains a line chart of the data collected with X axis representing time
The R script is called from within the Python script so no additional action is required. 
