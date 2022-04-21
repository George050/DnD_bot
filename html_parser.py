import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


url = 'https://musify.club/release/divinity-original-sin-2-ost-2017-922827'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('a', target="_blank")
spis = []
for i in soup.find_all('a', target="_blank"):
    spis.append(["https://musify.club{}".format(i.get('href')), i.get('download')])
music_spis = spis[:-2]


page = urlopen('http://dnd.su/spells/').read()
soup = BeautifulSoup(page)
soup.prettify()
spell_data = {}
for anchor in soup.findAll('a', href=True, title=True)[17:-1]:
    spell_data[anchor['title']] = 'http://dnd.su' + anchor['href']
print(spell_data)


