from src.util.earthquake_filter_utils import get_value_from_eid
from src.util.math_utils import haversine
from src.util.math_utils import date_time_diff_in_hours
import numpy as np
import pandas as pd

def earthquake_metric_function(df, eq1_event_id, eq2_event_id, W_mag, W_depth, W_distance, W_time):
    lat1 = get_value_from_eid(df, eq1_event_id, "Latitude")
    lat2 = get_value_from_eid(df, eq2_event_id, "Latitude")
    lon1 = get_value_from_eid(df, eq1_event_id, "Longitude")
    lon2 = get_value_from_eid(df, eq2_event_id, "Longitude")

    mag_diff = abs(get_value_from_eid(df, eq1_event_id, "xM") - get_value_from_eid(df, eq2_event_id, "xM"))
    depth_diff = abs(
        get_value_from_eid(df, eq1_event_id, "Depth(km)") - get_value_from_eid(df, eq2_event_id, "Depth(km)"))
    distance_diff = haversine(lat1, lon1, lat2, lon2)
    time_diff_hours = date_time_diff_in_hours(get_value_from_eid(df, eq1_event_id, "Datetime"),
                                              get_value_from_eid(df, eq2_event_id, "Datetime"))

    weighted_sum = (mag_diff * W_mag +
                    depth_diff * W_depth +
                    distance_diff * W_distance +
                    time_diff_hours * W_time)
    return weighted_sum


# W_mag, W_depth, W_distance, W_time
def vectorized_earthquake_metric_function(mag_diff, depth_diff, distance_diff, time_diff, weights):
    return (weights[0] * (10 ** mag_diff) +
            weights[1] * depth_diff +
            weights[2] * distance_diff +
            weights[3] * time_diff)


# Optimizer Function (Vectorized)
def optimize_metric_vectorized(weights, df):
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()

    W_mag, W_depth, W_distance, W_time = weights  # Unpack the weights list
    weights = np.array([W_mag, W_depth, W_distance, W_time])

    # Extract the relevant columns as NumPy arrays
    magnitudes = df_copy['xM'].values
    depths = df_copy['Depth(km)'].values
    latitudes = df_copy['Latitude'].values
    longitudes = df_copy['Longitude'].values
    date_times = pd.to_datetime(df_copy['Datetime'], format="%d/%m/%Y %H:%M:%S").values

    # Calculate pairwise differences using broadcasting
    mag_diff = np.abs(magnitudes[:, None] - magnitudes)
    depth_diff = np.abs(depths[:, None] - depths)

    # Calculate pairwise haversine distances
    lat_diff = np.radians(latitudes[:, None] - latitudes)
    lon_diff = np.radians(longitudes[:, None] - longitudes)
    a = np.sin(lat_diff / 2) ** 2 + np.cos(np.radians(latitudes))[:, None] * np.cos(np.radians(latitudes)) * np.sin(
        lon_diff / 2) ** 2
    distance_diff = 2 * 6371.0 * np.arcsin(np.sqrt(a))

    # Calculate pairwise time differences in hours
    time_diff = np.abs((date_times[:, None] - date_times).astype('timedelta64[h]').astype(float))

    # Calculate the metric for all pairs
    total_metric_value = vectorized_earthquake_metric_function(mag_diff, depth_diff, distance_diff, time_diff,
                                                               weights).sum()

    # Return the negative total metric value to minimize it
    return -total_metric_value

