import pytest
import os

def test_lookup_memento(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=False)
	dmanager.set_twitter_handle(r'm_nsiddique')
	output_path = os.path.join(configreader.intermediate, 'Mementos', 'm_nsiddique', 'desktop/web.archive.org/default/20191029182506.warc.gz')
	assert dmanager.lookup_memento(r'http://web.archive.org/web/20191029182506/http://twitter.com/m_nsiddique') == output_path
	assert dmanager.lookup_memento(r'http://web.archive.org/web/20200418015350/http://twitter.com/msiddique') == None

def test_write_memento(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=False)
	dmanager.set_twitter_handle(r'phonedude_mln')
	output_path = os.path.join(configreader.intermediate, 'Mementos', 'phonedude_mln', 'desktop/web.archive.org/default/20200601005425.warc.gz')
	assert dmanager.write_memento(r'http://web.archive.org/web/20200601005425/https://twitter.com/phonedude_mln') == True
	assert dmanager.lookup_memento(r'http://web.archive.org/web/20200601005425/https://twitter.com/phonedude_mln') == output_path

def test_read_memento(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=False)
	dmanager.set_twitter_handle(r'phonedude_mln') 
	assert dmanager.read_memento(r'http://web.archive.org/web/20200601005425/https://twitter.com/phonedude_mln') != None

def test_write_timemap(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=False)
	assert dmanager.write_timemap(r'https://twitter.com/test', r'This is a test timemap') == True

def test_read_timemap(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=False)
	assert dmanager.read_timemap('https://twitter.com/test') == [r'This is a test timemap']

def test_lookup_timemap(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=False)
	assert dmanager.lookup_timemap(r'https://twitter.com/m_nsiddique') == True

def test_write_follower_count(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=True)
	test_row = [{"MementoTimestamp": 20201130120000, "URI-M": r'http://web.archive.org/web/20200601005425/https://twitter.com/phonedude_mln', "FollowerCount": 100, "DateTime": 2020/11/30}]
	assert dmanager.write_follower_count(r'test', test_row) == True

def test_lookup_follower_count(datamager_connection):
	dmanager, configreader, constants = datamager_connection(parameters=True)
	assert dmanager.lookup_follower_count(r'test') ==True