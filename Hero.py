hero_name = ""


async def hero(name=""):
    global hero_name
    if name == "":
        return hero_name
    elif name == 123:
        hero_name = ""
    else:
        hero_name = name