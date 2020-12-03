#!/bin/sh
cd tests
python3 -m pytest tests_system_testing.py
python3 -m pytest tests_utils.py
python3 -m pytest tests_datamanager.py
python3 -m pytest tests_followeranalysis.py 
python3 -m pytest tests_followerparser.py 
python3 -m pytest tests_timemapdownloader.py