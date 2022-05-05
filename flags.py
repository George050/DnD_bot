flags = {}  # Словрь для хранения флагов для определнных действий пользователей


def flags_change(id, di='', de=''):  # Функция для изменения словаря с флагами
    global flags
    if di == '' and de == '':
        if id in flags:
            return flags[id]
        elif not id in flags:
            flags[id] = {"dice_flag": False,
                         "delete_flag": False}
            return flags[id]
    if di != '':
        flags[id]['dice_flag'] = di
    if de != '':
        flags[id]['delete_flag'] = de