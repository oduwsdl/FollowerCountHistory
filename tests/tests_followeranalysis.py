import pytest

def test_relative_analysis(follower_analysis_connection):
	fanalysis = follower_analysis_connection
	input = [{'MementoDatetime': '20180528235445', 'URIM': 'https://web.archive.org/web/20180528235445/https://twitter.com/m_nsiddique', 'FollowerCount': 31}, {'MementoDatetime': '20191029182506', 'URIM': 'https://web.archive.org/web/20191029182506/https://twitter.com/m_nsiddique', 'FollowerCount': 63}]
	assert fanalysis.relative_analysis(input) == True