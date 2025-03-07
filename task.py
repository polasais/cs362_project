#############################################
# task.py
#
# Implements:
#   1) conv_num(num_str)
#   2) my_datetime(num_sec)
#
# Follows all assignment restrictions.
#############################################

def conv_num(num_str):
    """
    Converts a string to an integer, float, or hexadecimal integer.
    Returns None for invalid formats.
    """

    if not isinstance(num_str, str) or not num_str.strip():
        return None

    num_str = num_str.strip().lower()

    if num_str.startswith("0x") or num_str.startswith("-0x"):
        return parse_hex(num_str)

    if "." in num_str:
        return parse_float(num_str)

    return parse_integer(num_str)


def parse_hex(num_str):
    """Converts a hex string (e.g., 0xFF or -0xAD) to decimal."""
    is_negative = num_str.startswith("-0x")
    hex_part = num_str[3:] if is_negative else num_str[2:]

    if not hex_part or any(c not in "0123456789abcdef" for c in hex_part):
        return None

    decimal_value = 0
    for c in hex_part:
        decimal_value = decimal_value * 16 + "0123456789abcdef".index(c)

    return -decimal_value if is_negative else decimal_value


def parse_float(num_str):
    """Converts a float string (e.g., '-123.45', '.45', '123.') to a float."""
    is_negative = num_str.startswith("-")
    num_str = num_str.lstrip("-")

    if num_str.count(".") > 1:
        return None  # Multiple decimal points → invalid

    left, right = num_str.split(".")
    if left and not left.isdigit():
        return None
    if right and not right.isdigit():
        return None

    integer_value = sum((ord(c) - ord('0')) * (10 ** i) for i, c in enumerate(reversed(left))) if left else 0
    fractional_value = sum((ord(c) - ord('0')) * (10 ** -(i + 1)) for i, c in enumerate(right))

    result = integer_value + fractional_value
    return -result if is_negative else result


def parse_integer(num_str):
    """Converts an integer string (e.g., '12345', '-6789') to an integer."""
    is_negative = num_str.startswith("-")
    num_str = num_str.lstrip("-")

    if not num_str.isdigit():
        return None

    integer_value = sum((ord(c) - ord('0')) * (10 ** i) for i, c in enumerate(reversed(num_str)))
    return -integer_value if is_negative else integer_value


def my_datetime(num_sec):
    """
    Converts an integer num_sec (seconds since 01-01-1970) into "MM-DD-YYYY".
    """

    days_since_epoch = num_sec // 86400

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    year, month, day = 1970, 1, 1

    while True:
        is_leap = my_datetime_helper_function(year)
        days_this_year = 366 if is_leap else 365
        if days_since_epoch >= days_this_year:
            days_since_epoch -= days_this_year
            year += 1
        else:
            break

    days_in_month[1] = 29 if my_datetime_helper_function(year) else 28

    for i in range(12):
        if days_since_epoch >= days_in_month[i]:
            days_since_epoch -= days_in_month[i]
            month += 1
        else:
            break

    day += days_since_epoch

    return f"{month:02d}-{day:02d}-{year}"


def my_datetime_helper_function(year):
    """Returns True if the year is a leap year, False otherwise."""
    if (year % 400) == 0:
        return True
    if (year % 100) == 0:
        return False
    if (year % 4) == 0:
        return True
    return False


def conv_endian(num, endian='big'):
    """Takes an integer (num) and converts it to a hexadecimal number."""
    negative = False
    if num[0] == '-':
        negative = True
        num = num(abs)
    hexadecimal = []
    while num % 16 != 0:
        num = num // 16
        remainder = num % 16
        hexadecimal.insert(0, str(remainder))
    for num in hexadecimal:
        if num == '10':
            num = 'A'
        elif num == '11':
            num = 'B'
        elif num == '12':
            num = 'C'
        elif num == '13':
            num = 'D'
        elif num == '14':
            num = 'E'
        elif num == '15':
            num = 'F'
    hexstring = ''
    for num in hexadecimal:
        hexstring += num
    if negative is True:
        hexstring = -hexstring
    