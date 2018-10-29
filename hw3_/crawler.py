import urllib.request as req
import re

def crawsite(address, numOfTags):
	page = getPage(address)
	tags = getTags(page, numOfTags)
	links = []
	for tag in tags:
                links += findLinks(getPage(tag))
	return links
	
def getPage(address):
	r = req.Request(address)
	html = ""
	with req.urlopen(r) as response:
		html = response.read()
		charset = re.search(r'charset=("?)(\S*)"', str(html))
		html = html.decode(charset.groups()[1])
	return html

def getTags(raw, numOfTags):
        e= re.compile('<a\s*href="(.*)"\s*class="ajax item')
        l = re.findall(e, raw)
        return l[:numOfTags]
		
def findLinks(raw):
	e = re.compile('lg-3 ">\s*<figure>\s*<a href="(.*)">')
	l = re.findall(e, raw)
	return l
