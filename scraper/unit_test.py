import pytest
from loc_scraper import scrape
from loc_scraper import process_page

fileindex: int = 1

def test_scrape_none():
	assert scrape(None) == -3

def test_process_page_none():
	with pytest.raises(Exception):
		process_page(None, fileindex)

def test_scrape_invalid_url():
	assert scrape("not_a_url") == -2

def test_process_page_invalid_url():
	with pytest.raises(Exception):
		process_page("not_a_url", fileindex)

def test_scrape_non_corpus_url():
	assert scrape("https://www.example.com/") == -2

def test_process_page_non_lit_url():
	with pytest.raises(Exception):
		process_page("https://www.example.com/", fileindex)

def test_scrape_sucess():
	assert scrape("https://www.loc.gov/books/?dates=1700/1799&fa=online-format:online+text%7Clanguage:english") == 0

def test_process_page_success():
	assert process_page("https://www.loc.gov/item/rbpe.10700800/", fileindex) == None