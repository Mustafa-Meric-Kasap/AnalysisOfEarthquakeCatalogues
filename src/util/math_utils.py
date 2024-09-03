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
    time_diff_h = abs((datetime1 - datetime2).total_seconds()) / 3600.
    return time_diff_h

