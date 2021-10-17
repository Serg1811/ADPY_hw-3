import requests
import bs4
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
pattern = rf"(({')+|('.join(KEYWORDS)})+)+"
res = requests.get('https://habr.com/ru/all/')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, features='html.parser')
articles = soup.find_all('article')
for article in articles:
    text = article.find().text.lower()
    link = 'https://habr.com' + article.find(class_='tm-article-snippet__title-link').attrs['href']
    if not re.search(pattern, text):
        res = requests.get(link)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, features='html.parser')
        body = soup.find(class_='tm-article-body')
        content = '\n'.join([p.text for p in body.find_all(re.compile("^(p|h2)"))])
        if not re.search(pattern, content):
            continue
    snippet = article.find('h2').text
    time = article.find('time').attrs['title']
    print(time, '-', snippet, '-', link)
