import requests
from collections import deque
from bs4 import BeautifulSoup

# Object intended to couple a URL with whether or not
# it is a page of written literature text
class ScraperObject:
	def __init__(self, URL, isLitPage):
		self.URL = URL
		self.isLitPage = isLitPage

# The main scraper method
# Takes in a starting URL and puts it in a deque. That URL
# is then popped off and the scraper begins traversing 
# through the pages. The end result should be text files
# containing the full written text of each piece of literature
# contained in a corpus along with entries in the database
# for the metadata about each piece of literature.
def scrape(startingURL, isText):
	q = deque()
	scrobj = ScraperObject(startingURL, isText)

	q.append(scrobj)

	# Extract full written text
	while len(q) > 0:
		scrobj = q.popleft()
		page = requests.get(scrobj.URL)
		soup = BeautifulSoup(page.content, "lxml")

		# Make sure the page actually contains text to extract before trying to do so
		if scrobj.isLitPage == True:
			results = soup.find(id = 'page-fulltext')
			text_elems = results.find_all('ammemxml')
			
			for elem in text_elems:
				print(elem.text)

			print()

			# Queue up the next page for further extraction
			nav_buttons = soup.findAll('a', class_ = 'next', attrs={'href'})

			scrobj = ScraperObject(nav_buttons[0].get('href'), True)

			if scrobj.URL != "#":
				q.append(scrobj)

			# for link in nav_buttons:
			# 	print(link.get('href'))

			# control = soup.find_all(class_ = 'control-section')
			# nav = control.find('div', role = 'navigation')

			# for nav_elems in nav:
			# 	next_page = nav_elems.find('a', class_ = 'next')['href']
			# 	print(next_page.text.strip())

	# Extract metadata
	print("\n-- Metadata --")

	page = requests.get(startingURL)
	soup = BeautifulSoup(page.content, "lxml")

	titles = soup.findAll('dt')
	content = soup.findAll('dd')

	for i in range(len(titles)):
		if titles[i].text.strip() == "Title":
			print("Title: " + content[i].text.strip())

		if titles[i].text.strip() == "Contributor Names":
			print("Author(s): " + content[i].text.strip())

	print("URL: " + startingURL)

scrape("https://www.loc.gov/resource/rbpe.1050020a/?sp=1&st=text", True)