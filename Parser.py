import random
import requests
from bs4 import BeautifulSoup
import pandas as pd


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                         ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
           'accept': '*/*'}
HOST = 'https://habr.com/ru/'


def get_url(params=None):
    while True:
        post = random.randint(1, 542766)
        url = f'https://habr.com/ru/post/{post}/'
        html = requests.get(url, headers=HEADERS, params=params)
        soup = BeautifulSoup(html.text, 'html.parser')
        title = soup.find('span', class_='post__title-text')
        try:
            s = title.text
            return url
        except:
            pass


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_info(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    title = soup.find('span', class_='post__title-text').text
    article = soup.find('div', class_='post__text post__text-html post__text_v1').text
    code = soup.find_all('pre')
    for i in code:
        article = article.replace(i.text, '')
    tags_soup = soup.find_all('a', class_='inline-list__item-link post__tag')
    tags = []
    for i in tags_soup:
        s = i.text.strip()
        tags.append(s)

    return title, article, tags


def work(root_of_txt):
    data = []
    for i in range(50):
        data1 = []
        URL = get_url()
        html = get_html(URL)
        title, article, tags = get_info(html)
        data1.append(URL)
        data1.append(title)
        data1.append(article)
        data1.append(tags)
        data.append(data1)

    filename = root_of_txt
    df = pd.DataFrame(data,
    columns=['link', 'title', 'body', 'tags'])
    df.to_csv(filename, index=False, sep='\t')


work(r'C:\Users\Темон3000\Desktop\1.txt')