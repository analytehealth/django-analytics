from datetime import timedelta
from decimal import Decimal


def average(numerator, denominator):
    """ Method to calculate and format an average safely """
    if not denominator:
        return "0.00"
    return "%.2f" % (numerator / Decimal(denominator))


def average_duration(total_duration, visits):
    """ Method to calculate and format an average duration safely """
    if not visits:
        seconds = 0
    else:
        seconds = int(round(total_duration / Decimal(visits)))
    duration = timedelta(seconds=seconds)
    return str(duration)


def percentage(numerator, denominator):
    """ Method to calculate and format a rate (%) safely """
    if not denominator:
        return "0.00%"
    val = (numerator / Decimal(denominator)) * 100
    return "%.2f%%" % val

def format_date(date_obj):
    return date_obj.strftime('%m/%d/%y')
