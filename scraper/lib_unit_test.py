import pytest
from libertyfund_scraper import scrape
from libertyfund_scraper import process_links
from libertyfund_scraper import process_page
from collections import deque

fileindex: int = 1

def test_scrape_none():
	assert scrape(None) == -3

def test_process_page_none():
	with pytest.raises(Exception):
		process_page(None, fileindex)

def test_process_links_no_list():
	assert process_links(None, fileindex, deque()) == 0

def test_process_links_no_deque():
	assert process_links(["example.com", "example.com"], fileindex, None) == 0

def test_process_links_empty_list():
	assert process_links([], fileindex, deque()) == 0

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