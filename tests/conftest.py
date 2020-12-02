import pytest
import os
import sys
import platform

if not __package__:
	sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fch.core.utils.constants import Constants
from fch.core.config.configreader import ConfigurationReader
from fch.core.datamanager import DataManager
from fch.follower.followeranalysis import FollowerAnalysis
from fch.follower.followerparser import FollowerParser

@pytest.fixture(scope="module")
def datamager_connection():
	constants = Constants()
	configreader = ConfigurationReader()
	if platform.system().lower() != "linux":
		configreader.intermediate = os.getcwd()
	dmanager = DataManager(configreader, constants) 
	def _change_config__output_dir(parameters):
		if parameters == True:
			if platform.system().lower() != "linux":
				configreader.intermediate = os.getcwd()
			else:
				configreader.out = "csv"
		return dmanager, configreader, constants
	return _change_config__output_dir

@pytest.fixture(scope="function")
def follower_analysis_connection(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=False)
	configreader.debug = True
	fanalysis = FollowerAnalysis("m_nsiddique", configreader, constants, dmanager)
	return fanalysis

@pytest.fixture(scope="function")
def follower_parser_connection(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=False)
	fparser = FollowerParser("m_nsiddique", constants, dmanager, configreader)	
	return fparser, dmanager