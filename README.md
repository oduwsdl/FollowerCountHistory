# Twitter Follower Count History via Internet Archives
This is a Python script that collects follower counts from the Internet Archives, given a Twitter user name. This script grabs the follower counts by identifying various CSS Selectors that match the follower count element on the historical Twitter pages for almost every major overhaul their page layout has gone through. The program only collects one data point per month by default.

## Output
A csv file noting the date of the archived Twitter page, the follower count for that date, and a link to the memento.
A csv file noting the date of the archived Twitter page, the reason follower count was not collected, and a link to the memento.
Optional: A line graph displaying the collected data.

The program will print to the console the date it is currently processing 'YYYYMMDDHHMMSS' and the action taken to show it's progress.

The program will assume any previously available csv file of the proper name contains the proper data that FollowerHist.py would generate and will refrain from asking the archive for that date again. Thus if the data is wrong, the program will not fix it.

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
$ pip install -r requirements.txt
$ ./FollowerHist.py [-h] [-g] [-e] [-p | -P] <twitter-username-without-@>
```

This will create a new folder with the name: <twitter-username-without-@> and create three files in this folder.
* A .csv file that contains the data collected with associated timestamps
* A .csv file that contains data for mementos follower count was not extracted from
* A .png file that contains a line chart of the data collected with X axis representing time
The R script is called from within the Python script, with the [-g] flag so no additional action is required.


To just create the graph from a csv file
```shell
$ git clone https://github.com/oduwsdl/FollowerCountHistory.git
$ cd FollowerCountHistory
$ Rscript --vanilla follower_count_linechart.R <twitter-username-without-@>
```

### Docker

We have published a docker image at `oduwsdl/fch` which can be used to run this tool as following:

```
$ docker container run --rm -it -v </PATH/TO/OUTPUT/FOLDER>:/app oduwsdl/fch [OPTIONS] <twitter-username-without-@>
```

### Options
```
-h	Help
-g	Create graph.
-p	Push to Internet Archive. Will only push if last memento is not within current month. 
        Need additional dependencies datetime and archivenow.	
-P      Push to all archives available through archivenow. 
        Will only push if last memento in Internet Archive is not within current month. 
        Need additional dependencies datetime and archivenow.	
-e      Collect follower count from every memento, not just once per month.
```
