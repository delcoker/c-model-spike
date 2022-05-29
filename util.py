import datetime as dt


def get_month_number(month):
    datetime_object = dt.datetime.strptime(month, "%B")
    month_number = datetime_object.month
    return month_number


def get_month_name(month_number):
    if month_number == 0:
        month_number = 12
    datetime_object = dt.datetime.strptime(str(month_number), "%m")
    month_name = datetime_object.strftime("%b")
    return month_name
