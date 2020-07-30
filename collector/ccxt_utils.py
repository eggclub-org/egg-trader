import time


def get_timeframe_unit_in_second(timeframe):
    timeframe_unit_in_second = 0

    time_unit = timeframe[-1]

    if len(timeframe) >= 2:
        time_value = int(timeframe[:-1])
    else:
        time_value = 1

    if time_unit == 'm':
        timeframe_unit_in_second = time_value * 60
    elif time_unit == 'h':
        timeframe_unit_in_second = time_value * 60 * 60
    elif time_unit == 'd':
        timeframe_unit_in_second = time_value * 60 * 60 * 24

    return timeframe_unit_in_second


def round_up_timeframe(timeframe, since=None, n_last_record=None):
    timeframe_unit = get_timeframe_unit_in_second(timeframe) * 1000

    if n_last_record:
        now = int(time.time()) * 1000
        since = now - n_last_record * timeframe_unit

    if timeframe_unit == 0:
        return since

    round_since = (since // timeframe_unit) * timeframe_unit

    if round_since < since:
        round_since += timeframe_unit

    return round_since
