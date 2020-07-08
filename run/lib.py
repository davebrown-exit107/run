'''Utility functions'''
import pendulum


def timestamp_to_datetime(timestamp):
    '''Convert a string to a datetime instance'''
    utc_time = pendulum.instance(timestamp)
    return utc_time


def find_timezone(tf, lat, lng):
    '''Find the timezone for a given set of coordinates'''
    lat = float(lat)
    lng = float(lng)

    try:
        timezone_name = tf.timezone_at(lng=lng, lat=lat)
        if timezone_name is None:
            timezone_name = tf.closest_timezone_at(lng=lng, lat=lat)
            # maybe even increase the search radius when it is still None
    except ValueError:
        print('no timezone found')
        # the coordinates were out of bounds

    return timezone_name
