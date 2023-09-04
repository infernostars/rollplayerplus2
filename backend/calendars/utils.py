from enum import Enum


class OffsetType(Enum):
    OFFSET_CONVERT = 1  # Convert dates by offsetting them [ex. Shift the Logotsai calendar to make it match up]
    START_YEAR_1 = 2  # Shifts dates around so the offset is ignored [ex. Logotsai calendar starts at Jan 1, 1 AD]
