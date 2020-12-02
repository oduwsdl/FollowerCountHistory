import pytest

def test_parse_mementos(follower_parser_connection):
	fparser, dmanager = follower_parser_connection
	dmanager.set_twitter_handle("m_nsiddique")
	output = [{'MementoDatetime': '20180528235445', 'URIM': 'https://web.archive.org/web/20180528235445/https://twitter.com/m_nsiddique', 'FollowerCount': 31}, {'MementoDatetime': '20191029182506', 'URIM': 'https://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique', 'FollowerCount': 63}]
	assert fparser.parse_mementos("https://twitter.com/m_nsiddique") == output