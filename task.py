def conv_num(num_str):
    num_str = num_str.lower()


def my_datetime(num_sec):
    month = 1
    day = 1
    year = 1970
    minutes = num_sec/60
    hours = minutes/60
    days = hours/24
    if days > 28:   # this if-statement is for linting error
        pass        # (as days, hours, minutes variables are unused), remove

    # calculate years and leap years
    print(f'{month}-{day}-{year}')


def my_datetime_helper_function(year):
    """
    Helper function for the my_datetime function.
    Returns True if inputted year is a leap year, False otherwise
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def conv_endian(num, endian='big'):
    pass
