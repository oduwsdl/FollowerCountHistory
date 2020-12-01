import subprocess
import pytest

def test_system():
	result = subprocess.run(['../fch/__main__.py', 'm_nsiddique'], stdout=subprocess.PIPE)
	assert result.stdout == b'MementoDatetime,URIM,FollowerCount,AbsGrowth,RelGrowth,AbsPerGrowth,RelPerGrowth,AbsFolRate,RelFolRate\r\n20180528235445,https://web.archive.org/web/20180528235445/https://twitter.com/m_nsiddique,31,0,0,0,0,0,0\r\n20191029182506,https://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique,63,32,32,103.23,103.23,0.0,0.0\r\n'