from cache import Cache

from bs4 import BeautifulSoup
import parsedatetime
from datetime import datetime
from time import mktime

cache = Cache()
html_doc = cache.get()

soup = BeautifulSoup(html_doc, 'html.parser')

articles = soup.find_all('li')
article = articles[0]
ticker = article.span.a.text
pub_date = article.div.div.contents[4]

cal = parsedatetime.Calendar()
time_struct, parse_status = cal.parse(pub_date)

pub_date = datetime.fromtimestamp(mktime(time_struct))
print "%s : %s" % (ticker, pub_date)