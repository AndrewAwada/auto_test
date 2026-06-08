def zune_days(days: int, is_leap: bool):
    while days > 365:
        if is_leap:
            if days > 366:
                days = days - 366
        else:
            days = days - 365
    return days
