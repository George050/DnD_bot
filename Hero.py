hero_name = {}  # Словарь для хранения выбранного персонажа у каждого пользователя


def hero(id, name=""):  # Функция для изменения словаря с персонажами или возвращения персонажа какого-то пользователя
    global hero_name
    if id in hero_name:
        pass
    else:
        hero_name[id] = ""
    if name == "":
        return hero_name[id]
    elif name == 123:
        hero_name[id] = ""
    else:
        hero_name[id] = name
