import requests
import time
from collections import deque
from bs4 import BeautifulSoup

# TODO add type hints
# TODO look into 'begins' library for beautifying the command-line interface

# The main scraper method
# Takes in a starting URL and puts it in a deque. That URL
# is then popped off and the scraper begins traversing 
# through the pages. The end result should be text files
# containing the full written text of each piece of literature
# contained in a corpus along with entries in the database
# for the metadata about each piece of literature.
def scrape(startingURL: str) -> None:
	q: object = deque()
	fileindex: int = 1

	# Load the starting page (assumed to be the result of a search) and begin parsing
	page: object = requests.get(startingURL)
	soup: object = BeautifulSoup(page.content, 'lxml')

	# Loop until we have exhausted the contents of this corpus
	while True:

		# Queue up each piece of literature on the page
		search_items: object = soup.findAll('li', class_ = ['item first', 'item']) # first result is a different name for whatever reason
		next_page: object = soup.find('a', class_ = 'next')

		for item in search_items:
			linksoup: object = BeautifulSoup(item.prettify(), 'lxml')
			links: object = linksoup.findAll('a')
			q.append(links[0].attrs['href'])
			print(links[0].attrs['href'])

		# Go through the queue of results, first extracting their metadata then the full text
		while len(q) > 0:
			litpage: str = q.popleft()
			page: object
			jsonpage: object

			try:
				page = requests.get(litpage + "?fo=json")
				page.raise_for_status()
			except Exception as err:
				print(f'Error occurred: {err}')
				print('Waiting 5 seconds then trying again...')
				time.sleep(5)
				page = requests.get(litpage + "?fo=json")
				jsonpage = page.json()
			else:
				jsonpage = page.json()

			fulltext_link: str
			#page = requests.get(litpage)
			soup = BeautifulSoup(page.content, 'lxml')

			# try:
			# 	for c in jsonpage.get('item').get('contributor_names'):
			# 		#print(list(c.keys())[0])
			# 		print(c)
			# except:
			# 	print("no contribs")

			for c in jsonpage.get('resources'):
				fulltext_link = c.get('fulltext_file')

			# for collections in jsonpage.get('item'):
			# 	try:
			# 		print(type(jsonpage.get('item')))
			# 		print(jsonpage.get)
			# 	except:
			# 		print("No contributors listed")

			#print(jsonpage.json()["item"]["contributors"])

			# Extract Metadata
			print("\n-- Metadata --")

			print("Title:")
			try:
				print("\t" + jsonpage.get('item').get('title'))
			except:
				print("\tNo title provided.")

			print("Contributor name(s):")
			try:
				for name in jsonpage.get('item').get('contributor_names'):
					print("\t" + name)
			except:
				print("\tNo contributors listed.")

			print("URL: " + litpage)

			# Extract written text
			#pagelinks = soup.findAll('a')

			page = requests.get(fulltext_link)
			soup = BeautifulSoup(page.content, 'xml')

			results: object = soup.find(name = 'text')
			text_elems: object = results.find_all('body')
			print(type(text_elems))

			filename: str = f"literature{fileindex}.txt"

			# Output text to file
			file: object = open(filename, "a")

			for elem in text_elems:
				file.write(elem.text)

			file.close()
			print("File " + filename + " written.")

			fileindex = fileindex + 1

		# Load up the next page of results, if there is one
		if next_page == None:
			break

		print("NEXT PAGE")
		page = requests.get(next_page.attrs['href'])
		soup = BeautifulSoup(page.content, 'lxml')

scrape("https://www.loc.gov/books/?fa=online-format%3Aonline+text&dates=1700%2F1799&st=list&c=25")
