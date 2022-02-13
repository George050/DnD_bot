hero_name = ""


def hero(name=""):
    global hero_name
    if name == "":
        return hero_name
    else:
        hero_name = name