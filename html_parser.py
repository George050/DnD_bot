import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


url = 'https://musify.club/release/divinity-original-sin-2-ost-2017-922827'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
spis = []
for i in soup.find_all('a', target="_blank"):
    spis.append(["https://musify.club{}".format(i.get('href')), i.get('download')])
music_spis = spis[:-2]


page = urlopen('http://dnd.su/spells/').read()
soup = BeautifulSoup(page)
soup.prettify()
spell_data = {}
for anchor in soup.findAll('a', href=True, title=True)[17:-1]:
    spell = anchor['title'][:anchor['title'].index('[') - 1]
    if spell[-1] == " ":
        spell = spell[:-1]
    spell_data[spell] = 'http://dnd.su' + anchor['href']

for i in spell_data:
    print(i, spell_data[i])


def lvl_cls_check(spell, hero_level, hero_class):
    url = spell_data[spell]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    level = soup.find_all('li', class_='size-type-alignment')[0].text.split()[0]
    classes = soup.find('ul', class_='params').find_all_next('li')[5].text.replace(',', '').split()
    if "Заговор" in level:
        level = 0
    level = int(level)
    if not (hero_class.lower() in classes):
        return classes
    elif hero_level < level:
        return level
    else:
        return True

