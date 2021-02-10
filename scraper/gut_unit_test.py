import pytest
import os
from gutenberg_scraper import scrape

def test_scrape_invalid_dir():
	os.environ['GB_FILES'] = '/home/fake_dir'
	assert scrape() == -1

def test_scrape_empty_dir():
	os.makedirs('/home/empty_dir/', exist_ok=True)
	os.environ['GB_FILES'] = '/home/empty_dir'
	assert scrape() == -2
	os.rmdir('/home/empty_dir')