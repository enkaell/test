from urllib.request import urlopen
from xml.etree.ElementTree import parse

var_url = urlopen('https://give-ur-xml.herokuapp.com/')
xmldoc = parse(var_url)

for item in xmldoc.iterfind('channel/item'):
    title = item.findtext('title')
    date = item.findtext('pubDate')
    link = item.findtext('link')

print(title)
print(date)
print(link)
print()
