# Twitter Follower Count History via Internet Archives
This is a Python script that collects follower counts from the Internet Archives, given a Twitter username. This script grabs the follower counts by identifying various CSS Selectors that match the follower count element on the historical Twitter pages for almost every major overhaul their page layout has gone through.

## Installation and Usage
'''shell
$ git clone https://github.com/okrand/FollowerCountHistory.git
$ cd FollowerCountHistory
$ python main.py <twitter-handle-without-@>
'''
This will create a new folder with the name: <twitter-handle-without-@> and create two files in this folder.
* A .csv file that contains the data collected with associated timestamps
* A .png file that contains a line chart of the data collected with X axis representing time