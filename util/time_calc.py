import time
import string

def timestamp_in(tm):
    current = time.time()
    total_secs = 0

    buffer = ""
    for char in tm:
        if char in string.digits:
            buffer += char
        else:
            if char == "s":
                total_secs += int(buffer)
            elif char == "m":
                total_secs += int(buffer) * 60
            elif char == "h":
                total_secs += int(buffer) * 60**2
            elif char == "d":
                total_secs += int(buffer) * 60**2 * 24

            buffer = ""

    return current + total_secs

def time_period_human_readable(tm):
    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    tm = int(tm)

    days = int(tm / (60**2 * 24))
    tm -= days * 60**2 * 24

    hours = int(tm / (60**2))
    tm -= hours * 60**2

    minutes = int(tm / 60)
    tm -= minutes * 60

    seconds = tm

    return str(days) + "d " + str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s"