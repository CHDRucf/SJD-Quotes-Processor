import requests
from collections import deque
from bs4 import BeautifulSoup

# The main scraper method
# Takes in a starting URL and puts it in a deque. That URL
# is then popped off and the scraper begins traversing 
# through the pages. The end result should be text files
# containing the full written text of each piece of literature
# contained in a corpus along with entries in the database
# for the metadata about each piece of literature.
def scrape(startingURL, isText):
	q = deque()
	fileindex = 1

	# Starting at the starting page (assumed to be the result of a search), queue up every result
	page = requests.get(startingURL)
	soup = BeautifulSoup(page.content, 'lxml')

	search_items = soup.findAll('li', class_ = ['item first', 'item']) # first result is a different name for whatever reason

	for item in search_items:
		linksoup = BeautifulSoup(item.prettify(), 'lxml')
		links = linksoup.findAll('a')
		q.append(links[0].attrs['href'])

	# Go through the queue of results, first extracting their metadata then the full text
	while len(q) > 0:
		litpage = q.popleft()
		page = requests.get(litpage)
		soup = BeautifulSoup(page.content, 'lxml')

		# Extract Metadata
		print("\n-- Metadata --")

		titles = soup.findAll('dt')
		content = soup.findAll('dd')

		for i in range(len(titles)):
			if titles[i].text.strip() == "Title":
				print("Title: " + content[i].text.strip())

			# TODO This currently only prints the first contributor if there's more than one
			if titles[i].text.strip() == "Contributor Names":
				print("Author(s): " + content[i].text.strip())

		print("URL: " + litpage)

		# Extract written text
		pagelinks = soup.findAll('a')

		page = requests.get(pagelinks[22].attrs['href'])
		soup = BeautifulSoup(page.content, 'xml')

		results = soup.find(name = 'text')
		text_elems = results.find_all('body')

		filename = f"literature{fileindex}"

		# Output text to file
		file = open(filename, "a")

		for elem in text_elems:
			file.write(elem.text)

		file.close()
		print("File " + filename + " written.")

		fileindex = fileindex + 1

scrape("https://www.loc.gov/books/?fa=online-format%3Aonline+text&dates=1700%2F1799&st=list&c=25", True)