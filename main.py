import datetime
from dateutil.parser import parse
from sqllite import insert_done, check_done


# gets starting time of taking pills, type of given interval for taking a pill (hour, min, sec), \
# interval for taking a pill,pill interval value, threshold(is one level smaller than pill interval type \
# e.g: pill_interval_type == hour then threshold == minute
def get_pill_time(start: str, pill_interval_type: str, pill_interval_value: int, threshold: int) -> dict:
    start_datetime = parse(start)
    do_it = None
    next_five = []
    last_take = None
    interval_timedelta = None
    next_pill = None
    threshold_timedelta = None

    start_stamp = int(round(start_datetime.timestamp()))
    now_stamp = int(round(datetime.datetime.now().timestamp()))
    start_now_diff = now_stamp - start_stamp

    # passed_intervals ==> number of passed intervals since the start

    if pill_interval_type == 'd':
        passed_intervals = (start_now_diff // (pill_interval_value * 24 * 60 * 60))
        last_take = start_datetime + datetime.timedelta(days=passed_intervals * pill_interval_value)
        interval_timedelta = datetime.timedelta(days=pill_interval_value)
        next_pill = last_take + interval_timedelta
        threshold_timedelta = datetime.timedelta(hours=threshold)

    elif pill_interval_type == 'h':
        passed_intervals = (start_now_diff // (pill_interval_value * 60 * 60))
        last_take = start_datetime + datetime.timedelta(hours=passed_intervals * pill_interval_value)
        interval_timedelta = datetime.timedelta(hours=pill_interval_value)
        next_pill = last_take + interval_timedelta
        threshold_timedelta = datetime.timedelta(minutes=threshold)

    elif pill_interval_type == 'm':
        passed_intervals = (start_now_diff // (pill_interval_value * 60))
        last_take = start_datetime + datetime.timedelta(minutes=passed_intervals * pill_interval_value)
        interval_timedelta = datetime.timedelta(minutes=pill_interval_value)
        next_pill = last_take + interval_timedelta
        threshold_timedelta = datetime.timedelta(seconds=threshold)

    next_take = last_take
    for i in range(6):
        next_take = next_take + interval_timedelta
        next_five.append(next_take.isoformat())

    if datetime.datetime.now() > next_pill - threshold_timedelta:

        if not check_done(next_pill.isoformat()):
            do_it = next_pill.isoformat()
            insert_done(next_pill.isoformat())

            res = {
                'do_it': do_it,
                'next': next_five[1:]
            }

        else:
            do_it = 'SENT'
            res = {
                'do_it': do_it,
                'next': next_five[1:]
            }

    else:
        do_it = None
        res = {
            'do_it': do_it,
            'next': next_five[:5]
        }

    # return res
    print(res)


if __name__ == '__main__':
    a = '2022-02-13T22:30:00'
    b = 'h'
    c = 1  # hours
    d = 50  # minutes
    get_pill_time(a, b, c, d)
