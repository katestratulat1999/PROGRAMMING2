import urllib.request as req
import re
import os

def getPage(address):
	r = req.Request(address)
	html = ""
	with req.urlopen(r) as response:
		html = response.read()
		charset = re.search(r'charset=("?)(\S*)"', str(html))
		html = html.decode(charset.groups()[1])
	return html

def getDate(raw):
        e = re.compile('data-time="\d*"\s*title="(.*?)\s*\d*:')
        l = re.search(e, raw)
        return l.group(1).strip()

def getTags(address, raw):
        tags = "@au None\n"
        tags += "@ti %s\n" % getTitle(raw)
        tags += "@da %s\n" % getDate(raw)
        tags += "@topic None\n"
        tags += "@url %s\n" % address
        return tags

def getTitleImg(raw):
	e = re.compile('mb-20">\s*<div class="image">\s*(.*)\s*</div>')
	l = re.search(e, raw)
	if l:
		return l.group(1).strip()
	else:
		return ""

def getTitle(raw):
	e = re.compile('class="post-title">\s*(.*)</h1>')
	l = re.search(e, raw)
	return l.group(1).strip()

def getBody(raw):
        e = re.compile('post-text">\s*(.*?)</div>')
        l = re.search(e, raw)
        return formatBody(l.group(1).strip())

def getBodyForRead(raw):
        e = re.compile('post-text">\s*(.*?)</div>')
        l = re.search(e, raw)
        return formatForRead(l.group(1).strip())
	
def formatBody(page):
	page = re.sub('<p.*?>\s*', '\n', page)
	page = re.sub('<.*?>', "", page)
	page = page.replace("&nbsp;", "")
	return page

def formatForRead(page):
        i = 0
        while True:
                i = page.find('src="', i) + 5
                if i != 4:
                        page = page[:i] + "http://gazeta-rvs.ru" + page[i:]
                else:
                        break
        return page

def createForRead(address):
        page = getPage(address)
        with open("template.html", 'r', encoding = "utf-8") as f:
                html = f.read()
        html = html.replace("titleimg", getTitleImg(page))
        html = html.replace("titletxt", getTitle(page))
        html = html.replace("bodytxt", getBodyForRead(page))
        if not os.path.exists("./htmlForRead"):
                os.makedirs("./htmlForRead")
        with open("./htmlForRead" + address[25:] + ".html", 'w', encoding = "utf-8") as f:
                f.write(html)
	
def createHtml(address, name):
        createForRead(address)
        page = getPage(address)
        title = getTitle(page)
        date = getDate(page)
        year = date[-4:]
        month = date[-7:-5]
        html = getTags(address, page)
        html += title
        html += getBody(page)
        if not os.path.exists("%s/plain/%s/%s" % (name, year, month)):
                os.makedirs("%s/plain/%s/%s" % (name, year, month))
                meta = "path\tauthor\theader\tcreated\tsphere\ttopic\tstyle\taudience_age\taudience_level\taudience_size\tsource\tpublication\tpubl_year\tmedium\tcountry\tregion\tlanguage\n"
                with open("%s/metadata.csv" % (name), 'w') as f:
                        f.write(meta)  
        with open('%s/plain/%s/%s/%s.txt' % (name, year, month, address[26:]), 'w', encoding = "utf-8") as f:
                f.write(html)
        print("%s IS DONE!" % address[26:])
        meta = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (address,'None', title, date, 'публицистика', 'None', 'нейтральный', 'н-возраст', 'н-уровень', 'районная', address, 'Газета РВС', year, 'газета', 'Россия', 'Динской район', 'ru')
        with open("%s/metadata.csv" % (name), 'a+') as f:
                f.write(meta)
