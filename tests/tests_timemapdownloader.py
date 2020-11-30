import pytest
import os
import sys

if not __package__:
	sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fch.core.utils.constants import Constants
from fch.core.config.configreader import ConfigurationReader
from fch.core.datamanager import DataManager
from fch.core.timemapdownloader import TimeMapDownloader

def test_fetch_timemap():
	constants = Constants()
	configreader = ConfigurationReader()
	dmanager = DataManager(configreader, constants)
	thandle = "ewarren"
	tmapdownloader = TimeMapDownloader(thandle, constants, dmanager, configreader)
	#assert tmapdownloader.fetch_timemap("https://twitter.com/m_nsiddique") == True	
	assert tmapdownloader.fetch_timemap("https://twitter.com/ewarren") == True
	# assert tmapdownloader.fetch_timemap("https://twitter.com/msiddique") == False		