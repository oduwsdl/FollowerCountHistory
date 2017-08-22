

from sys import argv
import subprocess
uname = argv[1]
call = "Rscript --vanilla follower_count_linechart.r " + uname
subprocess.call(call, shell=True)