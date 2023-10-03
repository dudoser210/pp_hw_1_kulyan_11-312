import os

import requests as req
from bs4 import BeautifulSoup

host = "https://habr.com"

page_count = 1

urls = []
while len(urls) < 100:
    r = req.get(host + '/ru/all/page' + str(page_count))
    soup = BeautifulSoup(r.content, 'html.parser')

    page_urls = list(
        filter(
            lambda link: ("company" in link or "post" in link) and "comments" not in link,
            map(
                lambda elem: host + elem['href'],
                filter(
                    lambda link: not link['href'].startswith("http"),
                    soup.body.find_all('a', href=True)
                )
            )
        )
    )

    for link in page_urls:
        urls.append(link)

    page_count += 1

try:
    os.mkdir('files')
except FileExistsError:
    pass

index = []

for i in range(len(urls)):
    link = urls[i]
    r = req.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')

    text = soup.body.find(id="post-content-body")

    index.append(link)

    file = open('files/%s.txt' % i, 'w')
    file.write(text.prettify())

file = open('index.csv', 'w')
for i in range(len(index)):
    link = index[i]
    file.write('"%s";"%s"\n' % (i, link))