# Twitter Follower Count History via Web Archives
Follower Count History is a Python module that collects Twitter follower count from the web archives using [MemGator](https://github.com/oduwsdl/MemGator) for a given Twitter handle. The module parses the follower count by identifying various CSS Selectors that match the follower count element on the historical Twitter pages for almost every major overhaul their page layout has gone through. The program collects all of the memento data points by default.

[1] Mohammed Nauman Siddique. 2020. Historical Twitter Follower Count Via Web Archives. (August 2020). Retrieved August 05, 2020 from https://ws-dl.blogspot.com/2020/08/2020-08-05-historical-twitter-follower.html

[2] Miranda Smith. 2018. Twitter Follower Count History via the Internet Archive. (March 2018). Retrieved July 25, 2020 from https://ws-dl.blogspot.com/2018/03/2018-03-14-twitter-follower-count.html

## Installation and Usage
### Dependencies
* Python 3
* bs4
* warcio
* requests
* R* (Optional: to create graph)

### Usage
```shell
$ git clone https://github.com/oduwsdl/FollowerCountHistory.git
$ cd FollowerCountHistory
$ pip install -r requirements.txt
$  ./__main__.py [-h] [--st] [--et] [--freq] [--out] <Twitter handle/ Twitter URL>
```
#### Install from pypi
```shell
$ pip install fch
$  fch [-h] [--st] [--et] [--freq] [--out] <Twitter handle/ Twitter URL>
```

To just create the graph from a csv file
```shell
$ Rscript twitterFollowerCount.R <CSV file path>
```

### Docker

We have published a docker image at [oduwsdl/fch](https://hub.docker.com/r/oduwsdl/fch) with the tag <b>2.0</b>, which can be used to run this tool as following:

```
$  docker container run --rm -it   -v <Output Directory>:/app  -u $(id -u):$(id -g)  oduwsdl/fch:2.0 [options] <Twitter Handle>
```

Example of output being mapped to the current directory

```
$  docker container run --rm -it -v $PWD:/app -u $(id -u):$(id -g) oduwsdl/fch:2.0 --out  --st=20200101000000 --et=20200331000000 --freq=2592000  joebiden
```

Example of docker command for generating follower graph

```
$ docker container run --rm -it -v $PWD:/app -u $(id -u):$(id -g) --entrypoint /bin/bash oduwsdl/fch:2.0
I have no name!@736a209b64d6:/app$ ./__main__.py --freq=2592000 joebiden| Rscript twitterFollowerCount.R
```
### Options
```
Follower Count History (fch)

positional arguments:
  thandle     Enter a Twitter handle/ URL

optional arguments:
  -h, --help  show this help message and exit
  --st        Memento start datetime (YYYYMMDDHHMMSS)
  --et         Memento end datetime (YYYYMMDDHHMMSS)
  --freq      Sampling frequency of mementos (in seconds)
  -f          Output file path (Supported Extensions: JSON and CSV)
```
* --st: Default is set to Twitter birth date (2006-03-21 12:00:00). It accepts the memento datetime in [RFC 8601](https://www.iso.org/iso-8601-date-and-time-format.html) fourteen digit variation.
* --et: Default is set to the current datetime. It accepts the memento datetime in [RFC 8601](https://www.iso.org/iso-8601-date-and-time-format.html) fourteen digit variation.
* --freq: Default is set to download all the mementos
* -f: Accepts JSON and CSV file paths for output. If no value is provided, output is returned to stdout in CSV format.

## Output

The program can generate output in JSON and CSV format. The -f option directs the output of CSV or JSON files to the supplied file path. By default, the module returns the outut in CSV format to the stdout.  

### Output Fields

Field| Description
---------|------------
MementoTimestamp |         memento datetime in [RFC 8601](https://www.iso.org/iso-8601-date-and-time-format.html) fourteen digit variation
URI-M            |         link to the memento
FollowerCount    |         follower count from the URI-M
AbsGrowth        |         follower count increase/decrease w.r.t. the first memento
RelGrowth	 | 	   follower Count increase/decrease w.r.t. the previous memento
AbsPerGrowth 	 |	   pecentage increase/decrease in follower count w.r.t. the first memento
RelPerGrowth	 | 	   pecentage increase/decrease in follower count w.r.t. the previous memento
AbsFolRate 	 |	   daily Twitter follower growth rate w.r.t. the first memento
RelFolRate	 | 	   daily Twitter follower growth rate w.r.t. the previous memento

### Sample Outputs
JSON Output
```json
[{
	"MementoDatetime": "20200101001959",
	"URIM": "https://web.archive.org/web/20200101001959/https://twitter.com/JoeBiden",
	"FollowerCount": 4048208
}, {
	"MementoDatetime": "20200131120028",
	"URIM": "https://web.archive.org/web/20200131120028/https://twitter.com/joebiden",
	"FollowerCount": 4142510
}, {
	"MementoDatetime": "20200301001210",
	"URIM": "https://web.archive.org/web/20200301001210/https://twitter.com/JoeBiden/",
	"FollowerCount": 4202148
}]
```

CSV Output
```csv
MementoDatetime,URIM,FollowerCount,AbsGrowth,RelGrowth,AbsPerGrowth,RelPerGrowth,AbsFolRate,RelFolRate
20200101001959,https://web.archive.org/web/20200101001959/https://twitter.com/JoeBiden,4048208,0,0,0,0,0,0
20200131120028,https://web.archive.org/web/20200131120028/https://twitter.com/joebiden,4142510,94302,94302,2.33,2.33,0.0358,0.0358
20200301001210,https://web.archive.org/web/20200301001210/https://twitter.com/JoeBiden/,4202148,153940,59638,3.8,1.44,0.0297,0.02339
```
### Output to stdout

```shell
$ fch --st=20200101000000 --et=20200331000000  --freq=2592000 joebiden
```

### Output to files

**Command to return output to the file path**

```shell
$ fch --st=20200101000000 --et=20200331000000  --freq=2592000 -f=output/joebiden.csv joebiden
$ fch --st=20200101000000 --et=20200331000000  --freq=2592000 -f=output/joebiden.json joebiden
```

**Command to create graphs for each handle**

```shell
$ Rscript twitterFollowerCount.R <file path>
```

* List of Graphs for each Twitter handle:

File Name| Description
---------|------------
`<Twitterhandle>`-follower-count.jpg|                shows Twitter follower growth over time
`<Twitterhandle>`-follower-growth-relative.jpg|      shows Twitter follower growth w.r.t. previous memento
`<Twitterhandle>`-follower-growth.jpg|               shows absolute number and pecentage Twitter follower growth w.r.t. to first memento
`<Twitterhandle>`-follower-perc-growth-relative.jpg| shows Twitter follower growth over time w.r.t. previous memento in percentage
`<Twitterhandle>`-follower-rate-relative.jpg|        shows new followers added per day w.r.t. previous memento
`<Twitterhandle>`-follower-rate.jpg|                 shows new followers added per day w.r.t. first memento

## Examples

* Command to find Twitter follower count for a Twitter handle from all the mementos since the account creation up until today
  * Output to stdout as CSV
  ```shell
  $  fch joebiden
  ```
  * Output as CSV file
  ```shell
  $  fch -f=joebiden.csv joebiden
  ```
* Command to find Twitter follower count for a Twitter handle with a monthly sampling of the the mementos since the account creation up until today
  ```
  Frequency = 3600*24*30
  Frequency = 2592000
  ```
* Output to stdout as CSV
  ```shell
  $  fch --freq=2592000 joebiden
  ```
  * Output as CSV file
  ```shell
  $  fch -f=joebiden.csv --freq=2592000 joebiden
  ```
* Command to find Twitter follower count for a Twitter handle with a monthly sampling of the the mementos within a specified start and end timestamp
  * Output to stdout as CSV
  ```shell
  $  fch --st=20200101000000 --et=20200331000000 --freq=2592000 joebiden
  ```
  * Output as CSV file
  ```shell
  $  fch.py -f=joebiden.csv --st=20200101000000 --et=20200331000000 --freq=2592000 joebiden
