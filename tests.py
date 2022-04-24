import requests
from bs4 import BeautifulSoup

url = 'https://musify.club/release/divinity-original-sin-2-ost-2017-922827'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
print(soup)