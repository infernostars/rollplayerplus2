import random

operations = ["+", "-", "/", "*"]  # supported operations in python
dice_error = None


def dice_error_handler(id, description, exception="none"):
    dice_error = [id, description]
    print(f"{id}: {description}")
    pass


class Dice:

    def __init__(self, amount, low, high, modifiers, imodifiers):
        self.amount = amount
        self.low = low
        self.high = high
        self.modifiers = modifiers
        self.imodifiers = imodifiers

    def generate_random_array(self):
        random_array = []
        for _ in range(self.amount):
            random_array.append(random.randint(self.low, self.high))
        return random_array

    def swap_extremes(self):
        self.low, self.high = self.high, self.low

    def roll(self):
        raw = self.generate_random_array()
        self.rolls = raw
        for i in self.modifiers:
            self.rolls = i.apply_bonus(self.rolls)
        for i in self.imodifiers:
            self.rolls = i.apply_bonus(self.rolls)
        return [[sum(raw), raw], [sum(self.rolls), self.rolls]]


class Bonus:
    def __init__(self, operation, amount):
        if operation in operations:
            self.operation = operation
        else:
            dice_error_handler("2a", f"operation \"{self.operation}\" is not a valid operation!", "none")
            return
        self.amount = int(amount)

    def apply_bonus(self, rolleddice):
        newRolls = []
        for i in rolleddice:
            newRolls.append(eval(f"{i} {self.operation} {self.amount}"))
        return newRolls


class MarkedBonus:
    def __init__(self, markers, operation, amount):
        self.markers = [int(numeric_string) - 1 for numeric_string in markers]
        if operation in operations:
            self.operation = operation
        else:
            dice_error_handler("2a", f"operation \"{self.operation}\" is not a valid operation!", "none")
            return
        self.amount = int(amount)

    def apply_bonus(self, rolleddice):
        newRolls = []
        print("h")
        for i in enumerate(rolleddice):
            if i[0] in self.markers:
                newRolls.append(eval(f"{i[1]} {self.operation} {self.amount}"))
            else:
                newRolls.append(i[1])
        print(newRolls)
        return newRolls


def iterate_until_marker(lst):
    for i in range(0, len(lst), 2):
        if str(lst[i]).startswith('i['):
            break
        yield lst[i:i + 2]


def dice_creator(string):
    remainingString = string
    createdDice = Dice(1, 1, 100, [], [])

    # initialization section completed
    if string == "":
        return createdDice
    if string == "d":
        return createdDice
    split_number = remainingString.split("d", 1)
    try:
        createdDice.amount = int(split_number[0])
        remainingString = split_number[1]
    except Exception as e:
        dice_error_handler("0a", f"amount of dice could not be coerced into an int", e)
        return 0
    if createdDice.amount <= 0:
        dice_error_handler("0b", f"you cannot roll {createdDice.amount} dice, you need at least one dice!", "none")
        return 1

    # amount section completed

    split_str = re.split('([^0-9\.]+)', remainingString)

    if ":" in remainingString:  # if there's smth like 2d10:15
        try:
            createdDice.low = int(split_str[0])
        except Exception as e:
            dice_error_handler("1a", "lower bound could not be coerced into an int", e)
            return 1_00
        try:
            createdDice.high = int(split_str[2])
        except Exception as e:
            dice_error_handler("1b", "upper bound could not be coerced into an int", e)
            return 1_01
        split_str = split_str[3:]
    else:  # smth like just 2d15
        try:
            createdDice.high = int(split_str[0])
        except Exception as e:
            dice_error_handler("1c", "upper bound could not be coerced into an int", e)
            return 1_02
        split_str = split_str[1:]
    if createdDice.low > createdDice.high:
        createdDice.swap_extremes()

    # bounds section completed

    for pair in iterate_until_marker(split_str):
        createdDice.modifiers.append(Bonus(pair[0], pair[1]))

    regex = r"i\[(.*?)\]"
    matches = re.findall(regex, string)  # initial string should be fine here

    for markerPair in matches:
        splitPair = markerPair.split(";")
        toMatch = splitPair[0].split(",")
        splitOperation = re.split('([^0-9\.]+)', splitPair[1])
        print(splitOperation)
        createdDice.imodifiers.append(MarkedBonus(toMatch, splitOperation[1], splitOperation[2]))

    # done! :D

    return createdDice