from datetime import date, datetime, timedelta


def monday_on_or_before(the_date: date):
    """
    Return the date of the Monday in the week of the given date.

    :param the_date: The date to find the date of the Monday for.
    :rtype: date
    """
    return the_date - timedelta(days=the_date.weekday())


def monday_on_or_after(the_date: date):
    """
    Return the date of the Monday in the week of the given date.

    :param the_date: The date to find the date of the Monday for.
    :rtype: date
    """
    return the_date + timedelta(days=-the_date.weekday(), weeks=the_date.weekday() > 1)


def date_to_datetime(the_date: date):
    """
    Convert the given date to a datetime instance.

    :param the_date: The date to convert.
    :rtype: datetime
    """
    return datetime(
        the_date.year, the_date.month, the_date.day
    )
