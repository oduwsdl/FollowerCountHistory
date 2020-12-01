import pytest
import os
import sys
import datetime

if not __package__:
	sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fch.core.utils.constants import Constants
from fch.core.utils.util_functions import Utils

from fch.core.config.configreader import ConfigurationReader
from fch.core.datamanager import DataManager


'''
Happy Case: Test memento_to_epochtime()
'''

def test_memento_to_epochtime():
	assert Utils.memento_to_epochtime("20201128121212") == 1606565532
	assert Utils.memento_to_epochtime("19700101000000") == 0

'''
Sad Case: Test memento_to_epochtime()
'''

def test_malformed_memento_to_epochtime():
	assert Utils.memento_to_epochtime("20201128") == None
	assert Utils.memento_to_epochtime("abc") == None

'''
Happy Case: Test epochtime_to_memento()
'''

def test_epochtime_to_memento():
	assert Utils.epochtime_to_memento(1606565532) == "20201128121212"
	assert Utils.epochtime_to_memento(0) == "19700101000000"

'''
Sad Case: Test epochtime_to_memento()
'''

def test_malformed_epochtime_to_memento():
	assert Utils.epochtime_to_memento(-1) == "19691231235959"
	assert Utils.epochtime_to_memento("123") == None

'''
Happy Case: Test get_turl_info
'''

def test_get_turl_info():
	assert Utils.get_turl_info("https://twitter.com/m_nsiddique") == {'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'default', 'wrep': ''}
	assert Utils.get_turl_info("https://twitter.com/m_nsiddique?lang=en") == {'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'en', 'wrep': ''}
	assert Utils.get_turl_info("https://twitter.com/m_nsiddique/with_replies") == {'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'default', 'wrep': 'with_replies_'}
	assert Utils.get_turl_info("https://twitter.com/m_nsiddique/with_replies?lang=en") == {'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'en', 'wrep': 'with_replies_'}
	assert Utils.get_turl_info("https://twitter.com/m_nsiddique/status/1") == {'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'default', 'wrep': ''}
	assert Utils.get_turl_info("http://twitter.com/m_nsiddique") == {'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'default', 'wrep': ''}

'''
Happy Case: Test get_turl_info
'''

def test_get_murl_info():
	assert Utils.get_murl_info("http://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique") == {'domain': 'desktop', 'handle': 'm_nsiddique', 'TwitterURL': 'https://twitter.com/m_nsiddique', 'lang': 'default', 'wrep': '',  'archive': 'web.archive.org', 'timestamp': '20191029182506'}
	assert Utils.get_murl_info("http://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique?lang=en") == {'archive': 'web.archive.org', 'timestamp': '20191029182506', 'TwitterURL': 'https://twitter.com/m_nsiddique?lang=en', 'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'en', 'wrep': ''}
	assert Utils.get_murl_info("http://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique/with_replies") == {'archive': 'web.archive.org', 'timestamp': '20191029182506', 'TwitterURL': 'https://twitter.com/m_nsiddique/with_replies', 'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'default', 'wrep': 'with_replies_'}
	assert Utils.get_murl_info("http://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique/with_replies?lang=en") == {'archive': 'web.archive.org', 'timestamp': '20191029182506', 'TwitterURL': 'https://twitter.com/m_nsiddique/with_replies?lang=en', 'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'en', 'wrep': 'with_replies_'}
	assert Utils.get_murl_info("http://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique/status/1") == {'archive': 'web.archive.org', 'timestamp': '20191029182506', 'TwitterURL': 'https://twitter.com/m_nsiddique/status/1', 'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'default', 'wrep': ''}
	assert Utils.get_murl_info("http://web.archive.org/web/20191029182506/http://twitter.com/m_nsiddique") == {'archive': 'web.archive.org', 'timestamp': '20191029182506', 'domain': 'desktop', 'handle': 'm_nsiddique', 'TwitterURL': 'http://twitter.com/m_nsiddique', 'domain': 'desktop', 'handle': 'm_nsiddique', 'lang': 'default', 'wrep': ''}	

'''
Happy Case: Test get_timerange
'''

def test_get_timerange():
	constants = Constants()
	configreader = ConfigurationReader()
	assert Utils.get_timerange(constants, configreader) == {"mintime": 20060321120000, "maxtime": int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))}

'''
Happy Case: Test parse_timemap
'''

def test_parse_timemap():
	constants = Constants()
	configreader = ConfigurationReader()
	dmanager = DataManager(configreader, constants)
	assert Utils.parse_timemap(dmanager, constants, "https://twitter.com/m_nsiddique") == [{'datetime': 'Mon, 28 May 2018 23:54:45 GMT',  'rel': 'first memento', 'uri': 'https://web.archive.org/web/20180528235445/https://twitter.com/m_nsiddique'}, {'datetime': 'Tue, 29 Oct 2019 18:25:06 GMT',  'rel': 'last memento',  'uri': 'https://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique'}]