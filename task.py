def conv_num(num_str):
    pass


def my_datetime(num_sec):
    month = 1
    day = 1
    year = 1970
    minutes = num_sec/60
    hours = minutes/60
    days = hours/24
    # calculate years and leap years
    print(f'{month}-{day}-{year}')


def my_datetime_helper_function(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def conv_endian(num, endian='big'):
    pass
