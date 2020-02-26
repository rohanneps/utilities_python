from bs4 import BeautifulSoup
import requests

def getSourceCode(url):
	validUrlPrefix = ['http','https']
	def getCorrectUrlSchema(url):
		urlPrefix = url.split(':')[0]
		if urlPrefix not in validUrlPrefix:
			url = 'http://' + url
		return url
	correctUrl = getCorrectUrlSchema(url)
	return requests.get(correctUrl)

def getStrippedHtml(htmlContent):
	if str(htmlContent)=='nan' and type(htmlContent)==float:
		htmlContent = ''
	soup = BeautifulSoup(htmlContent,"html.parser")
	for script in soup(["script", "style"]):
		script.extract()    # rip it out

	# get text
	text = soup.get_text()

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# drop blank lines
	strippedHtml = '\n'.join(chunk for chunk in chunks if chunk)
	
	return (strippedHtml.replace('\n', ' ').replace('  ',' '))