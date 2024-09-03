import numpy as np
from datetime import datetime
def haversine(lat1: float, lon1: float, lat2: float, lon2: float, r = 6371.0):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Applying haversine formula
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = np.sin(delta_lat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    # Calculate the distance
    distance = c * r
    return distance

def date_time_diff_in_hours(datetime1, datetime2):
    # Check if the inputs are numpy.datetime64; if so, handle them accordingly
    if isinstance(datetime1, np.datetime64) and isinstance(datetime2, np.datetime64):
        # Calculate the absolute difference in seconds
        time_diff_seconds = np.abs((datetime1 - datetime2).astype('timedelta64[s]').astype(int))
    else:
        # Otherwise, assume they are Python datetime objects and handle them as before
        time_diff_seconds = abs((datetime1 - datetime2).total_seconds())

    # Convert the difference from seconds to hours
    time_diff_h = time_diff_seconds / 3600.0
    return time_diff_h
