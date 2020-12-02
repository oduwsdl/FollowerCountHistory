import pytest
import os
import sys

if not __package__:
	sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fch.core.timemapdownloader import TimeMapDownloader

def test_fetch_timemap(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=False)
	thandle = "ewarren"
	tmapdownloader = TimeMapDownloader(thandle, constants, dmanager, configreader)
	assert tmapdownloader.fetch_timemap("https://twitter.com/ewarren") == True
