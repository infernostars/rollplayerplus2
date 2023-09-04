import math

from backend.calendars.utils import OffsetType

offset = 23064  # days from calendar epoch to January 1st, 1 AD [Gregorian]


# Every 30 days, add one to the month marker. (30 days)
# Every 12 months, add one to the year marker. (360 days)
# Every 18 years, add one to the generation marker. (6480 days) (18 years)
# Every 6 generations, add one to the saeculum marker. (38880 days) (108 years)
# Every 24 saeculum, add one to the eon marker. (933120 days) (2592 years)

def logotsai_calendar(days: int, mode: OffsetType):
    if mode == OffsetType.OFFSET_CONVERT:
        days += offset

    if days < 0:
        polarity = False
        days = abs(days)
    else:
        polarity = True

    eons = math.floor(days / 933120)
    days -= eons * 933120
    saeculum = math.floor(days / 38880)
    days -= saeculum * 38880
    generations = math.floor(days / 6480)
    days -= generations * 6480
    years = math.floor(days / 360)
    days -= years * 360
    months = math.floor(days / 30)
    days -= months * 30

    if not polarity:
        return f"-{eons}.{saeculum}.{generations}.{years}.{months}.{days}"
    else:
        return f"{eons}.{saeculum}.{generations}.{years}.{months}.{days}"
