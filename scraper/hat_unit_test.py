import pytest
from selenium import webdriver
from selenium.webdriver import Chrome
from hathitrust_scraper import scrape
from hathitrust_scraper import process_page

fileindex: int = 1

chromeopts = webdriver.ChromeOptions()
chromeopts.headless = True
chromeopts.add_argument('window-size=1920x1080')
prefs = {"download.default_directory" : "/tmp/scraper-downloads/",
	 	 "download.prompt-for-download" : False,
	 	 "directory_upgrade" : True}
chromeopts.add_experimental_option('prefs', prefs)
browser = Chrome(chrome_options=chromeopts)

def test_scrape_none():
	assert scrape(None) == -3

def test_process_page_none():
	with pytest.raises(Exception):
		process_page(None, fileindex, browser)

def test_process_page_no_browser():
	with pytest.raises(Exception):
		process_page(["https://www.example.com/", "example", "ex"], fileindex, None)

def test_scrape_invalid_url():
	assert scrape("not_a_url") == -2

def test_process_page_invalid_url():
	with pytest.raises(Exception):
		process_page(["not_a_url", 'none', 'none'], fileindex, browser)

def test_scrape_non_corpus_url():
	assert scrape("https://www.example.com/") == -2

def test_process_page_non_lit_url():
	with pytest.raises(Exception):
		process_page(["https://www.example.com/", "example", "ex"], fileindex, browser)

def test_scrape_sucess():
	assert scrape("https://catalog.hathitrust.org/Search/Home?fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&page=1&pagesize=20&ft=ft") == 0

def test_process_page_success():
	assert process_page(['https://catalog.hathitrust.org/Record/000584038?filter%5B%5D=publishDateTrie%3A%5B%2A%20TO%201755%5D&fqor-language%5B%5D=English&fqor-language%5B%5D=English%2C%20Middle%20%281100-1500%29&fqor-language%5B%5D=English%2C%20Old%20%28ca.%20450-1100%29&fqor-format%5B%5D=Book&ft=ft', 'Miscellanies ... collected by John Aubrey.', 'Aubrey, John, 1626-1697'], fileindex, browser) == None