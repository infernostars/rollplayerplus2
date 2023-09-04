from enum import Enum
from typing import List


class FormattingMode(Enum):
    DEFAULT = 0
    LIST_ONLY = 1
    SUM_ONLY = 2
    ROWS = 3


def format_dice_roll(mode: FormattingMode, roll: list):
    match mode:
        case FormattingMode.DEFAULT:
            return f"{roll[0]} (total: {format_dice_roll(FormattingMode.LIST_ONLY, roll)})"
        case FormattingMode.LIST_ONLY:
            return ", ".join([f"{x}" for x in roll[1]])
        case FormattingMode.SUM_ONLY:
            return roll[0]
        case FormattingMode.ROWS:
            # thanks chatgpt
            # Initialize an empty string to store the formatted result
            formatted_string = ""

            # Iterate through the input list
            for i, item in enumerate(roll[1]):
                # Add the item to the formatted string
                formatted_string += str(item)

                # Check if we need to add a comma and a newline
                if i < len(roll[1]) - 1:
                    # Add a comma if it's not the last item
                    formatted_string += ", "

                    # Add a newline every 10 items
                    if (i + 1) % 10 == 0:
                        formatted_string += "\n"

            return formatted_string



