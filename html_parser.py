import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


url = 'https://musify.club/release/divinity-original-sin-2-ost-2017-922827' # ссылка на сайт
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
spis = []  # список с ссылками и названиями треков
for i in soup.find_all('a', target="_blank"):
    spis.append(["https://musify.club{}".format(i.get('href')), i.get('download')])
music_spis = spis[:-2]


page = urlopen('http://dnd.su/spells/').read()  # ссылка на сайт с заклинаниями
soup = BeautifulSoup(page)
soup.prettify()
spell_data = {}
spell_spis = []  # список с Русским названием заклинания и ссылка на него
for anchor in soup.findAll('a', href=True, title=True)[17:-1]:
    spell = anchor['title'][:anchor['title'].index('[') - 1]
    spell = spell.strip()
    spell_data[spell.capitalize()] = 'http://dnd.su' + anchor['href']
    spell_spis.append(spell)


def lvl_cls_check(spell, hero_level, hero_class):
    # функция для проверки возможности добавления персонажу данного заклинания
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

