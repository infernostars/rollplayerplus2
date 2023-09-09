import re

from backend.classes.dice_formatting_mode import autoformatter, format_dice_roll
from backend.utils.rolling import DiceError, dice_creator


def process_tag_string(s):
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
        s = s.replace('[' + match + ']', roll)
        s = s.replace("\\[", "[").replace("\\]", "]") # remove extra formatting
    return s
