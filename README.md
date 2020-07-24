# Twitter Follower Count History via Web Archives
This is a Python module that collects Twitter follower count from the web archives using [MemGator](https://github.com/oduwsdl/MemGator), given a Twitter user name. This module grabs the follower counts by identifying various CSS Selectors that match the follower count element on the historical Twitter pages for almost every major overhaul their page layout has gone through. The program collects all of the data points by default.

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
* warcio
* requests

*optional

### Usage
```shell
$ git clone https://github.com/oduwsdl/FollowerCountHistory.git
$ cd FollowerCountHistory
$ pip install -r requirements.txt
$  fch [-h] [--st] [--et] [--freq] [--out | --debug] <twitter-username-without-@>
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

We have published a docker image at [oduwsdl/fch](https://hub.docker.com/r/oduwsdl/fch), which can be used to run this tool as following:

```
$ docker container run --rm -it -v </OUTPUT/DIR>:/app/<TWITTER_HANDLE> oduwsdl/fch [OPTIONS] <TWITTER_HANDLE>
```

### Options
```
Follower Count History (fch)

positional arguments:
  thandle     Enter a Twitter handle

optional arguments:
  -h, --help  show this help message and exit
  --st        Memento start datetime format (in RFC 1123 datetime format)
  --et        Memento end datetime (in RFC 1123 datetime format)
  --freq      Sampling frequency of mementos(in seconds)
  --out       Path for follower count output in CSV format
  --debug     Debug Mode
```
