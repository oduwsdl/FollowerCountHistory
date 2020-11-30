import pytest
import os
import sys

if not __package__:
	sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from fch.core.utils.constants import Constants
from fch.core.config.configreader import ConfigurationReader
from fch.core.datamanager import DataManager


def test_lookup_memento():
	dmanager = DataManager(ConfigurationReader(), Constants()) 
	dmanager.set_twitter_handle(r'm_nsiddique')
	assert dmanager.lookup_memento(r'http://web.archive.org/web/20191029182506/http://twitter.com/m_nsiddique') == r'/tmp/Mementos/m_nsiddique/desktop/web.archive.org/default/20191029182506.warc.gz'
	assert dmanager.lookup_memento(r'http://web.archive.org/web/20200418015350/http://twitter.com/msiddique') == None

def test_write_memento():
	dmanager = DataManager(ConfigurationReader(), Constants()) 
	dmanager.set_twitter_handle(r'phonedude_mln')
	assert dmanager.write_memento(r'http://web.archive.org/web/20200601005425/https://twitter.com/phonedude_mln') == True
	assert dmanager.lookup_memento(r'http://web.archive.org/web/20200601005425/https://twitter.com/phonedude_mln') == r'/tmp/Mementos/phonedude_mln/desktop/web.archive.org/default/20200601005425.warc.gz'

def test_read_memento():
	dmanager = DataManager(ConfigurationReader(), Constants())
	memento_content = b'HTTP/1.1 200 OK\r\nServer: nginx/1.15.8\r\nDate: Mon, 30 Nov 2020 16:52:55 GMT\r\nContent-Type: text/html;charset=ut...solve: 224.612 (4)\n  PetaboxLoader3.datanode: 161.535 (4)\n  CDXLines.iter: 28.501 (3)\n  load_resource: 191.911\n-->'
	dmanager.set_twitter_handle(r'phonedude_mln') 
	assert dmanager.read_memento(r'http://web.archive.org/web/20200601005425/https://twitter.com/phonedude_mln') == memento_content

def test_write_timemap():
	dmanager = DataManager(ConfigurationReader(), Constants())
	assert dmanager.write_timemap(r'https://twitter.com/test', r'This is a test timemap') == True

def test_read_timemap():
	dmanager = DataManager(ConfigurationReader(), Constants())
	assert dmanager.read_timemap('https://twitter.com/test') == [r'This is a test timemap']

def test_lookup_timemap():
	dmanager = DataManager(ConfigurationReader(), Constants()) 
	assert dmanager.lookup_timemap(r'https://twitter.com/m_nsiddique') == True

def test_write_follower_count():
	configreader = ConfigurationReader()
	configreader.out = "/tmp/"
	dmanager = DataManager(configreader, Constants()) 
	test_row = [{"MementoTimestamp": 20201130120000, "URI-M": r'http://web.archive.org/web/20200601005425/https://twitter.com/phonedude_mln', "FollowerCount": 100, "DateTime": 2020/11/30}]
	assert dmanager.write_follower_count(r'test', test_row) == True

def test_lookup_follower_count():
	configreader = ConfigurationReader()
	configreader.out = "/tmp/"
	dmanager = DataManager(configreader, Constants()) 	
	assert dmanager.lookup_follower_count(r'test') ==True