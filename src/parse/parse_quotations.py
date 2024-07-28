import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd


ua = UserAgent()

headers = {
    'accept': 'application/json, text/plain, */*',
    'user-Agent': ua.google,
}

quotations = {}

url = f'https://time365.info/aforizmi/temi/kurenie'
req = requests.get(url, headers=headers).text
soup = BeautifulSoup(req, 'lxml')
all_quotations = soup.find('div', class_='card-body').find_all('blockquote')
identifier = 0
for i in all_quotations:
    identifier += 1
    if i.find('p') is not None and i.find('cite') is not None:
        quotations[identifier] = [i.find('cite').text, i.find('p').text]
    # print(i.text + '\n')

df = pd.DataFrame([i for i in quotations.values()], columns=['author', 'comment'])
df.to_csv('quotations.csv')
