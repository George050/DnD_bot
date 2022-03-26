hero_name = {}


def hero(id, name=""):
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
