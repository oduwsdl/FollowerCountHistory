import pytest
import os
import sys

if not __package__:
	sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fch.core.utils.constants import Constants
from fch.core.config.configreader import ConfigurationReader
from fch.core.datamanager import DataManager
from fch.follower.followerparser import FollowerParser

def test_parse_mementos():
	constants = Constants()
	conf_reader = ConfigurationReader()
	dmanager = DataManager(conf_reader, constants)
	dmanager.set_twitter_handle("m_nsiddique")
	fparser = FollowerParser("m_nsiddique", constants, dmanager, conf_reader)
	assert fparser.parse_mementos("https://twitter.com/m_nsiddique") == [{'MementoDatetime': '20180528235445', 'URIM': 'https://web.archive.org/web/20180528235445/https://twitter.com/m_nsiddique', 'FollowerCount': 31}, {'MementoDatetime': '20191029182506', 'URIM': 'https://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique', 'FollowerCount': 63}]