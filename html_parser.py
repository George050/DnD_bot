import requests
from bs4 import BeautifulSoup


url = 'https://musify.club/release/divinity-original-sin-2-ost-2017-922827'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('a', target="_blank")
spis = []
for i in soup.find_all('a', target="_blank"):
    spis.append(["https://musify.club{}".format(i.get('href')), i.get('download')])
music_spis = spis[:-2]

