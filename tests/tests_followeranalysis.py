import pytest
import os
import sys

if not __package__:
	sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fch.core.utils.constants import Constants
from fch.core.config.configreader import ConfigurationReader
from fch.core.datamanager import DataManager
from fch.follower.followeranalysis import FollowerAnalysis

def test_relative_analysis():
	constants = Constants()
	configreader = ConfigurationReader()
	dmanager = DataManager(configreader, constants)
	fanalysis = FollowerAnalysis("m_nsiddique", configreader, constants, dmanager)
	input = [{'MementoDatetime': '20180528235445', 'URIM': 'https://web.archive.org/web/20180528235445/https://twitter.com/m_nsiddique', 'FollowerCount': 31}, {'MementoDatetime': '20191029182506', 'URIM': 'https://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique', 'FollowerCount': 63}]
	assert fanalysis.relative_analysis(input) == True