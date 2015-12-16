from cache import Cache

from bs4 import BeautifulSoup

cache = Cache()
html_doc = cache.get()

soup = BeautifulSoup(html_doc, 'html.parser')

articles = soup.find_all('li')
article = articles[0]
ticker = article.span.a.text
pub_date = article.div.div.contents[4]