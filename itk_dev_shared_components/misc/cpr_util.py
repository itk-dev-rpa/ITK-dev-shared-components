"""This module contains helper functions regarding cpr numbers."""

from datetime import date


def get_age(cpr: str, current_date: date = date.today()) -> int:
    """Get the age of a person based on their cpr number
    using the 7th digit to infer the century.

    Args:
        cpr: The cpr number in the format 'ddmmyyxxxx'.
        current_date: The date where the age is calculated from. Defaults to the current date.

    Returns:
        The age in integer years based on the cpr number.

    Raises:
        ValueError: If the given cpr is not in 'ddmmyyxxxx' format.
    """
    if len(cpr) != 10 or not cpr.isnumeric():
        raise ValueError("The given CPR number is not in 'ddmmyyxxxx' format.")

    # A dictionary mapping from a year (0-99) and control digit (0-9) to a century.
    # https://cpr.dk/media/12066/personnummeret-i-cpr.pdf
    # The keys of the dict corespond to the control digit.
    # The first value of the tuples is the cutoff year. If the input year is equal to or below the first value
    # the first century is used. If the year is above the first value, the second century is used.
    # E.g. If the control is 4 and the year is smaller or equal to 36 -> 2000-2036
    # E.g. If the control is 7 and the year is larger than 57 -> 1858-1899
    cpr_reg = {
        0: (99, 1900, '-'),
        1: (99, 1900, '-'),
        2: (99, 1900, '-'),
        3: (99, 1900, '-'),
        4: (36, 2000, 1900),
        5: (57, 2000, 1800),
        6: (57, 2000, 1800),
        7: (57, 2000, 1800),
        8: (57, 2000, 1800),
        9: (36, 2000, 1900),
    }

    day = int(cpr[0:2])
    month = int(cpr[2:4])
    year = int(cpr[4:6])
    control = int(cpr[6])

    t = cpr_reg[control]
    if year <= t[0]:
        year += t[1]
    else:
        year += t[2]

    birthdate = date(year, month, day)

    age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))

    return age
