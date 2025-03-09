#############################################
# task.py
#
# Implements:
#   1) conv_num(num_str) with helper functions
#   2) my_datetime(num_sec) with helper function
#   3) conv_endian(num, endian='big') with helper function
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

    # Left part of .
    integer_value = 0
    if left:
        for i, c in enumerate(reversed(left)):
            digit_value = ord(c) - ord('0')
            integer_value += digit_value * (10 ** i)

    # Right part of .
    fractional_value = 0.0  # Ensure float type
    for i, c in enumerate(right):
        digit_value = ord(c) - ord('0')
        fractional_value += digit_value * (10 ** -(i + 1))

    result = integer_value + fractional_value
    return -result if is_negative else result


def parse_integer(num_str):
    """Converts an integer string (e.g., '12345', '-6789') to an integer."""
    is_negative = num_str.startswith("-")
    num_str = num_str.lstrip("-")

    if not num_str.isdigit():
        return None

    integer_value = 0
    for i, c in enumerate(reversed(num_str)):
        digit_value = ord(c) - ord('0')
        place_value = 10 ** i
        integer_value += digit_value * place_value

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


def convert_to_hex(num):
    """Converts a positive integer to a hexadecimal string."""
    hexadecimal = []
    while num > 0:
        remainder = num % 16
        hexadecimal.insert(0, str(remainder))
        num = num // 16

    hexastring = ''
    for num in hexadecimal:
        if num == '10':
            hexastring += 'A'
        elif num == '11':
            hexastring += 'B'
        elif num == '12':
            hexastring += 'C'
        elif num == '13':
            hexastring += 'D'
        elif num == '14':
            hexastring += 'E'
        elif num == '15':
            hexastring += 'F'
        else:
            hexastring += str(num)
    return hexastring


def conv_endian(num, endian='big'):
    """Converts an int to a hex string in either big or little endian form."""
    if endian != 'big' and endian != 'little':
        return None

    negative = False
    if num < 0:
        negative = True
        num = abs(num)

    hexastring = convert_to_hex(num)
    # Add a 0 if it's an uneven integer length.
    if len(hexastring) % 2 != 0:
        hexastring = "0" + hexastring

    if len(hexastring) % 2 != 0:
        hexastring = "0" + hexastring  # Ensure even length

    if endian == 'big':
        # Big Endian: return the hex string w/ spaces between every two digits.
        num_pairs = [hexastring[i:i+2] for i in range(0, len(hexastring), 2)]
        new_hex = " ".join(num_pairs)

    elif endian == 'little':
        # Little Endian: Reverse the hex string and reverse the pairs.
        num_pairs = [hexastring[i:i+2] for i in range(0, len(hexastring), 2)]
        new_hex = " ".join(reversed(num_pairs))

    if negative:
        new_hex = '-' + new_hex
    return new_hex
