import random


class Dices:
    def __init__(self, dice, quantity, bonus):
        self.dice = dice
        self.quantity = int(quantity)
        self.bonus = bonus

    def get_roll(self):
        dice_number = int(self.dice[2:])
        if "-" in self.bonus:
            bonus_number = -(int(self.bonus[1:]))
        elif "+" in self.bonus:
            bonus_number = int(self.bonus[1:])
        else:
            bonus_number = int(self.bonus)
        all_numbers = ""
        result = int(0)
        for i in range(self.quantity):
            number = random.randint(1, dice_number)
            if i != 0:
                all_numbers += "+ "
            if number == 1 or number == dice_number:
                all_numbers += "<u>{}</u> ".format(str(number))
            else:
                all_numbers += "{} ".format(str(number))
            result += number
        if bonus_number < 0:
            all_numbers += "- {}".format(str(bonus_number)[1:])
        else:
            all_numbers += "+ {}".format(bonus_number)
        result += bonus_number
        all_numbers += "\n<u>{}</u>".format(result)
        return all_numbers

