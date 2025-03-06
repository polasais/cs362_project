#############################################
# task.py
#
# Implements:
#   1) conv_num(num_str)
#   2) my_datetime(num_sec)
#   3) conv_endian(num, endian='big')
#
# without using any forbidden functions:
#   - int(), float(), hex(), eval(), literal_eval()
#   - datetime or similar libraries.
#############################################


def conv_num(num_str):
    """
    Converts a string into a base-10 integer, floating-point number, or hexadecimal integer.
    Returns None for invalid inputs.
    Requirements:
      - Must handle: integers, floats, 0x-prefixed hex (case-insensitive).
      - Must return int for integer/hex, float for decimal.
      - Negative numbers indicated by '-' (e.g., -123, -0xFF).
      - No hex floats (e.g., 0xFF.02 -> invalid).
      - Strings with multiple decimals or invalid chars -> None.
      - Must NOT use int(), float(), hex(), eval(), literal_eval().
    Examples:
      conv_num('12345') -> 12345
      conv_num('-123.45') -> -123.45
      conv_num('.45') -> 0.45
      conv_num('123.') -> 123.0
      conv_num('0xAD4') -> 2772
      conv_num('-0xAD4') -> -2772
      conv_num('0xAZ4') -> None
      conv_num('12.3.45') -> None
    """

    # 1) Basic checks
    if not isinstance(num_str, str) or not num_str.strip():
        return None

    num_str = num_str.strip().lower()

    ######################################
    # 2) Check for hex prefix: '0x' or '-0x'
    ######################################
    if num_str.startswith("0x") or num_str.startswith("-0x"):
        # Hex must be an integer (no decimal points allowed)
        if "." in num_str:
            return None

        is_negative = num_str.startswith("-0x")
        # Extract just the portion after '0x' or '-0x'
        hex_part = num_str[3:] if is_negative else num_str[2:]
        if not hex_part:  # nothing after '0x'
            return None

        # Validate hex digits
        valid_hex_digits = "0123456789abcdef"
        for ch in hex_part:
            if ch not in valid_hex_digits:
                return None

        # Convert manually from hex -> decimal
        decimal_val = 0
        for ch in hex_part:
            decimal_val = decimal_val * 16 + valid_hex_digits.index(ch)

        return -decimal_val if is_negative else decimal_val

    ######################################
    # 3) Handle decimal or integer
    ######################################
    if num_str.count(".") > 1:
        return None  # multiple decimal points -> invalid

    # Check sign
    is_negative = num_str.startswith("-")
    if is_negative:
        num_str = num_str[1:]  # remove leading '-'

    # If it contains a decimal point, parse as float
    if "." in num_str:
        left, right = num_str.split(".")
        # left part can be empty (e.g. ".45") => 0.x
        # right part can be empty (e.g. "123.") => 123.0

        # Validate left part (if not empty) is digits only
        if left and not all(c.isdigit() for c in left):
            return None
        # Validate right part (if not empty) is digits only
        if right and not all(c.isdigit() for c in right):
            return None

        # Convert left side manually
        int_part = 0
        for c in left:
            int_part = int_part * 10 + (ord(c) - ord('0'))

        # Convert right side manually
        frac_part = 0.0
        for i, c in enumerate(right, start=1):
            digit = (ord(c) - ord('0'))
            frac_part += digit * (10 ** -i)

        result = int_part + frac_part
        return -result if is_negative else result

    else:
        # No decimal => parse as integer
        if not all(c.isdigit() for c in num_str):
            return None

        value = 0
        for c in num_str:
            value = value * 10 + (ord(c) - ord('0'))

        return -value if is_negative else value


def my_datetime(num_sec):
    """
    Converts a non-negative integer num_sec (seconds since 01-01-1970) into "MM-DD-YYYY".
    Requirements:
      - No datetime or date libraries.
      - Must handle leap years.
      - Always return in MM-DD-YYYY format (zero-padded).
    Examples:
      my_datetime(0) -> '01-01-1970'
      my_datetime(123456789) -> '11-29-1973'
      my_datetime(9876543210) -> '12-22-2282'
      my_datetime(201653971200) -> '02-29-8360'
    """

    # 1 day = 86400 seconds
    days_since_epoch = num_sec // 86400

    # Days in each month (by default, Feb=28; we adjust for leap years)
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    year = 1970
    month = 1
    day = 1

    # Subtract whole years
    while True:
        is_leap = my_datetime_helper_function(year)
        days_this_year = 366 if is_leap else 365
        if days_since_epoch >= days_this_year:
            days_since_epoch -= days_this_year
            year += 1
        else:
            break

    # Adjust Feb based on leap year
    days_in_month[1] = 29 if my_datetime_helper_function(year) else 28

    # Subtract whole months
    for i in range(12):
        if days_since_epoch >= days_in_month[i]:
            days_since_epoch -= days_in_month[i]
            month += 1
        else:
            break

    # Remaining days belong to the current month
    day += days_since_epoch

    # Format zero-padded: MM-DD-YYYY
    return f"{month:02d}-{day:02d}-{year}"


def my_datetime_helper_function(year):
    """
    Returns True if 'year' is a leap year, False otherwise.
    Leap Year Rules:
      - divisible by 400 => leap
      - divisible by 100 => not leap
      - divisible by 4 => leap
      - else -> not leap
    """
    if (year % 400) == 0:
        return True
    if (year % 100) == 0:
        return False
    if (year % 4) == 0:
        return True
    return False


def conv_endian(num, endian='big'):
    """
    Converts an integer 'num' to a hexadecimal string in either 'big' or 'little' endian.
    Returns None for invalid 'endian'.
    Each byte must be two hex characters, separated by spaces.
    Must handle negative values (prefixed with '-').
    Forbidden to use hex(), to_bytes(), etc.
    Examples:
      conv_endian(954786, 'big') -> '0E 91 A2'
      conv_endian(954786) -> '0E 91 A2'
      conv_endian(-954786, 'big') -> '-0E 91 A2'
      conv_endian(954786, 'little') -> 'A2 91 0E'
      conv_endian(-954786, 'little') -> '-A2 91 0E'
      conv_endian(num=954786, endian='small') -> None
    """

    if endian not in ('big', 'little'):
        return None

    is_negative = (num < 0)
    num = abs(num)

    # Special case for zero
    if num == 0:
        # Single byte "00"
        bytes_list = ["00"]
    else:
        # Manually convert to hex (uppercase)
        hex_digits = "0123456789ABCDEF"
        hex_str = ""
        temp = num
        while temp > 0:
            remainder = temp % 16
            hex_str = hex_digits[remainder] + hex_str
            temp //= 16

        # Ensure even number of hex digits
        if len(hex_str) % 2 != 0:
            hex_str = "0" + hex_str

        # Split into bytes of 2 chars each
        bytes_list = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]

    # Reverse byte order if little-endian
    if endian == 'little':
        bytes_list.reverse()

    # Join with spaces
    result = " ".join(bytes_list)

    return f"-{result}" if is_negative else result
