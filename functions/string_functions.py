import datetime


def sortdict(e):
    return e['time']


def parse_done_time(input: str) -> datetime.timedelta:
    """
    Parses the input string representing the done time for a race. We expect something like this:
        01:23:45.6789
    which represents 1h 23m 45.6789s

    Unfortunately we may get any sort of crazy input.

    Parameters
    ----------
    input : str
        The user input, hopefully something sane

    Returns
    -------
    datetime.timedelta
        A measure of how long the race took
    """
    if not isinstance(input, str):
        emessage = f"Expected time input of type str. Found type {type(input)}"
        raise Exception(emessage)

    input = input.replace(",", ":")
    input = input.replace("h", ":")
    input = input.replace("m", ":")
    input = input.replace("s", ":")

    if not 0 < input.count(":") < 3:
        emessage = f"Expected time in the format of hh:mm:ss.xxxx or mm:ss.xxxx. Found {input}"
        raise Exception(emessage)

    ##Split the time by colons
    hours = 0
    minutes = 0
    seconds = 0
    time_split = input.split(':')
    seconds = time_split[-1]
    minutes = time_split[-2]
    if len(time_split) == 3:
        hours = time_split[0]

    try:
        hours = int(hours)
        assert 24 > hours >= 0

        minutes = int(minutes)
        assert 60 > minutes >= 0

        seconds = float(seconds)
        assert 60 > seconds >= 0

    except Exception as e:
        emessage = f"Time can't be 24+ hours or have more than 59 minutes or seconds. Found {input}"
        raise Exception(emessage)
    donetime = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return donetime
