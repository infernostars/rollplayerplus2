import random
import re
import time

from backend.classes.dice_formatting_mode import autoformatter, format_dice_roll
from backend.utils.rolling import DiceError, dice_creator


def process_tag_string(s, args):
    matches2 = re.findall(r'\{([^\\\]]*?\|[^\\\]]*?)\}', s)
    for match in matches2:
        split = match.split("|")
        try:
            val = args[int(split[0]) - 1]
        except:
            val = split[1]
        s = s.replace('{' + match + '}', val, 1)
    matches3 = re.findall(r'\{([^\\\]]*?)\}', s)
    for match in matches3:
        try:
            val = args[int(match) - 1]
        except:
            val = ""
        s = s.replace('{' + match + '}', val, 1)
    matches = re.findall(r'\[([^\\\]]*?)\]', s)
    for match in matches:
        dice, dice_formatting_mode = autoformatter(match)
        print(dice)
        try:
            dice_obj = dice_creator(dice)
            dice_result = dice_obj.roll()
        except DiceError as e:
            raise e
        roll = format_dice_roll(dice_formatting_mode, dice_result[1])
        s = s.replace('[' + match + ']', roll, 1)
    s = s.replace("\\{", "{").replace("\\}", "}")
    s = s.replace("\\[", "[").replace("\\]", "]")
    s = s.replace("\\n", "\n")
    return s
