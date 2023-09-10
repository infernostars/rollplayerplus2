import random
import re
import time
from enum import Enum
from typing import List

operations = ["+", "-", "/", "*"]  # supported operations in python


class DiceType(Enum):
    NORMAL = 0
    GAUSSIAN = 1


class DiceError(Exception):
    def __init__(self, message, id):
        super().__init__(message)
        self.id = id

def dice_error_handler(id, error, exc):
    raise DiceError(error, id)

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b


def unlerp(a: float, b: float, v: float) -> float:
    """Inverse Linar Interpolation, get the fraction between a and b on which v resides.
    Examples
    --------
        0.5 == inv_lerp(0, 100, 50)
        0.8 == inv_lerp(1, 5, 4.2)
    """
    return (v - a) / (b - a)


def remap(i_min: float, i_max: float, o_min: float, o_max: float, v: float) -> float:
    """Remap values from one linear scale to another, a combination of lerp and inv_lerp.
    i_min and i_max are the scale on which the original value resides,
    o_min and o_max are the scale to which it should be mapped.
    Examples
    --------
        45 == remap(0, 100, 40, 50, 50)
        6.2 == remap(1, 5, 3, 7, 4.2)
    """
    return lerp(o_min, o_max, unlerp(i_min, i_max, v))


def random_gaussian(min, max):
    mu = (min + max) / 2
    sigma = (max - min) / 5
    return round(random.gauss(mu, sigma), 2)

class Bonus:

    def __init__(self, operation, amount):
        if operation in operations:
            self.operation = operation
        else:
            dice_error_handler("2a", f"operation \"{self.operation}\" is not a valid operation!", "none")
            return 2_00
        self.amount = int(amount)

    def apply_bonus(self, rolleddice):
        new_rolls = []
        for i in rolleddice:
            new_rolls.append(eval(f"{i} {self.operation} {self.amount}"))
        return new_rolls


class MarkedBonus:
    def __init__(self, markers, operation, amount):
        self.markers = [int(numeric_string) - 1 for numeric_string in markers]
        if operation in operations:
            self.operation = operation
        else:
            dice_error_handler("2a", f"operation \"{self.operation}\" is not a valid operation!", "none")
            return 2_00
        self.amount = int(amount)

    def apply_bonus(self, rolleddice):
        new_rolls = []
        for i in enumerate(rolleddice):
            if i[0] in self.markers:
                new_rolls.append(eval(f"{i[1]} {self.operation} {self.amount}"))
            else:
                new_rolls.append(i[1])
        return new_rolls


class Dice:

    def __init__(self, amount: int, low: int, high: int, modifiers: List[Bonus], imodifiers: List[MarkedBonus], rolltype: DiceType):
        self.amount = amount
        self.low = low
        self.high = high
        self.modifiers = modifiers
        self.imodifiers = imodifiers
        self.rolltype = rolltype

    def generate_random_array(self):
        random_array = []
        for _ in range(self.amount):
            random_array.append(random.randint(self.low, self.high))
        return random_array

    def generate_random_gaussian_array(self):
        random_array = []
        for _ in range(self.amount):
            random_array.append(random_gaussian(self.low, self.high))
        return random_array

    def generate_max_array(self):
        random_array = []
        for _ in range(self.amount):
            random_array.append(self.high)
        return random_array

    def generate_min_array(self):
        random_array = []
        for _ in range(self.amount):
            random_array.append(self.low)
        return random_array

    def swap_extremes(self):
        self.low, self.high = self.high, self.low

    def roll(self):
        random.seed(time.time_ns())
        match self.rolltype:
            case DiceType.NORMAL:
                raw = self.generate_random_array()
            case DiceType.GAUSSIAN:
                raw = self.generate_random_gaussian_array()
        self.rolls = raw
        for i in self.modifiers:
            self.rolls = i.apply_bonus(self.rolls)
        for i in self.imodifiers:
            self.rolls = i.apply_bonus(self.rolls)
        return [[sum(raw), raw], [sum(self.rolls), self.rolls]]

    def roll_max(self):
        raw = self.generate_max_array()
        self.rolls = raw
        for i in self.modifiers:
            self.rolls = i.apply_bonus(self.rolls)
        for i in self.imodifiers:
            self.rolls = i.apply_bonus(self.rolls)
        return [[sum(raw), raw], [sum(self.rolls), self.rolls]]

    def roll_min(self):
        raw = self.generate_min_array()
        self.rolls = raw
        for i in self.modifiers:
            self.rolls = i.apply_bonus(self.rolls)
        for i in self.imodifiers:
            self.rolls = i.apply_bonus(self.rolls)
        return [[sum(raw), raw], [sum(self.rolls), self.rolls]]


def iterate_until_marker(lst):
    for i in range(0, len(lst), 2):
        if str(lst[i]).startswith('i['):
            break
        yield lst[i:i + 2]


def dice_creator(string):
    remaining_string = string
    created_dice = Dice(1, 1, 100, [], [], DiceType.NORMAL)

    # initialization section completed
    if remaining_string.startswith("g"):
        created_dice.rolltype = DiceType.GAUSSIAN
        remaining_string = remaining_string[1:]
    if remaining_string == "":
        return created_dice
    if remaining_string == "d":
        return created_dice
    split_number = remaining_string.split("d", 1)
    print(split_number)
    try:
        if split_number[0] == "":
            created_dice.amount = 1
        else:
            created_dice.amount = int(split_number[0])
        remaining_string = split_number[1]
    except Exception as e:
        dice_error_handler("0a", f"amount of dice could not be coerced into an int", e)
        return 0
    if created_dice.amount <= 0:
        dice_error_handler("0b", f"you cannot roll {created_dice.amount} dice, you need at least one dice!", "none")
        return 1

    # amount section completed

    split_str = re.split('([^0-9\.]+)', remaining_string)

    if ":" in remaining_string:  # if there's smth like 2d10:15
        try:
            created_dice.low = int(split_str[0])
        except Exception as e:
            dice_error_handler("1a", "lower bound could not be coerced into an int", e)
            return 1_00
        try:
            created_dice.high = int(split_str[2])
        except Exception as e:
            dice_error_handler("1b", "upper bound could not be coerced into an int", e)
            return 1_01
        split_str = split_str[3:]
    else:  # smth like just 2d15
        try:
            created_dice.high = int(split_str[0])
        except Exception as e:
            dice_error_handler("1c", "upper bound could not be coerced into an int", e)
            return 1_02
        split_str = split_str[1:]
    if created_dice.low > created_dice.high:
        created_dice.swap_extremes()

    # bounds section completed

    for pair in iterate_until_marker(split_str):
        created_dice.modifiers.append(Bonus(pair[0], pair[1]))

    regex = r"i\[(.*?)\]"
    matches = re.findall(regex, string)  # initial string should be fine here

    for markerPair in matches:
        split_pair = markerPair.split(";")
        to_match = split_pair[0].split(",")
        split_operation = re.split('([^0-9\.]+)', split_pair[1])
        created_dice.imodifiers.append(MarkedBonus(to_match, split_operation[1], split_operation[2]))

    # done! :D

    return created_dice