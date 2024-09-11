import numpy as np
import pandas as pd
from src.util import earthquake_filter_utils
from src.util import math_utils

def lat_lon_to_cartesian(lat, lon, R=6371.0):
    # Convert latitude and longitude from degrees to radians
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)

    # Calculate x, y, z coordinates
    x = R * np.cos(lat_rad) * np.cos(lon_rad)
    y = R * np.cos(lat_rad) * np.sin(lon_rad)
    z = R * np.sin(lat_rad)

    return np.array([x, y, z])


def spherical_vector(lat1, lon1, lat2, lon2):
    # Convert points to Cartesian coordinates
    p1 = lat_lon_to_cartesian(lat1, lon1)
    p2 = lat_lon_to_cartesian(lat2, lon2)

    # Calculate Cartesian difference vector
    d_cartesian = p2 - p1

    # The resulting vector contains x, y, and z components
    return d_cartesian


# This function adds cartesian coordinate system components as new columns to the df
def lat_lon_to_cartesian_vectorized(df, R=6371.0):
    lat_rad = np.radians(df['Latitude'].values)
    lon_rad = np.radians(df['Longitude'].values)

    x = R * np.cos(lat_rad) * np.cos(lon_rad)
    y = R * np.cos(lat_rad) * np.sin(lon_rad)
    z = R * np.sin(lat_rad)

    df_copy = df.copy()
    df_copy['X'] = x
    df_copy['Y'] = y
    df_copy['Z'] = z

    return df_copy

def distance_filter_numpy(df, event_id, radius_km=10):
    event_lat = earthquake_filter_utils.get_value_from_eid(df, event_id, "Latitude")
    event_lon = earthquake_filter_utils.get_value_from_eid(df, event_id, "Longitude")

    # Get latitudes and longitudes as NumPy arrays
    lats = df['Latitude'].values
    lons = df['Longitude'].values

    # Vectorized haversine computation
    distances = math_utils.haversine(event_lat, event_lon, lats, lons)

    # Filter distances within the radius
    mask = distances <= radius_km
    return df[mask]


def past_earthquakes_filter_numpy(df, event_id, num_earthquakes=30):
    event_datetime = earthquake_filter_utils.get_value_from_eid(df, event_id, "Datetime")

    # Convert 'Datetime' column to NumPy array for fast access
    datetimes = df['Datetime'].values

    # Ensure 'datetimes' is in np.datetime64 format
    if datetimes.dtype != 'datetime64[ns]':
        datetimes = datetimes.astype('datetime64[ns]')

    # Filter for earthquakes that happened before the target event
    past_indices = np.where(datetimes < event_datetime)[0]

    # Raise an error if fewer than num_earthquakes exist
    if len(past_indices) < num_earthquakes:
        raise ValueError(f"PAST EARTHQUAKE ERROR: {event_id} with only {len(past_indices)} past earthquakes available.")

    # Sort the past earthquakes in chronological order (oldest to newest)
    sorted_indices = past_indices[np.argsort(datetimes[past_indices])]

    # Select the most recent 'num_earthquakes' from the sorted past earthquakes
    selected_indices = sorted_indices[-num_earthquakes:]

    # Get the row corresponding to the event itself (to append it later)
    event_row = df[df['Event ID'] == event_id]

    # Concatenate the past earthquakes and the target event
    result_df = pd.concat([df.iloc[selected_indices], event_row], ignore_index=True)

    # Return the resulting DataFrame (length will be num_earthquakes + 1)
    return result_df

def time_filter_numpy(df, event_id, years=30):
    event_datetime = earthquake_filter_utils.get_value_from_eid(df, event_id, "Datetime")

    # Ensure the event_datetime is in NumPy datetime64 format
    if not isinstance(event_datetime, np.datetime64):
        event_datetime = np.datetime64(event_datetime)

    hours = int(years * 365.25 * 24)

    # Calculate the cutoff time using hours
    cutoff_time = event_datetime - np.timedelta64(hours, 'h')

    datetimes = df['Datetime'].values

    if datetimes.dtype != 'datetime64[ns]':
        datetimes = datetimes.astype('datetime64[ns]')

    # Perform the filtering: Get earthquakes before the event but after the cutoff time
    mask = (datetimes <= event_datetime) & (datetimes >= cutoff_time)
    return df[mask]


def space_time_filter_numpy(df, event_id, radius_km=10, past_years=30, num_earthquakes=30):
    filtered_df = distance_filter_numpy(df, event_id, radius_km)
    filtered_df = time_filter_numpy(filtered_df, event_id, past_years)
    filtered_df = past_earthquakes_filter_numpy(filtered_df, event_id, num_earthquakes)
    return filtered_df.iloc[:-1], filtered_df.iloc[-1] # past_s_earthquakes, target earthquake


def get_row_property_numpy(df, idx_array):
    # Convert columns to NumPy arrays for faster access
    event_ids = df['Event ID'].values
    magnitudes = df['xM'].values
    depths = df['Depth(km)'].values
    X_coords = df['X'].values
    Y_coords = df['Y'].values
    Z_coords = df['Z'].values
    dates = df['Datetime'].values

    # Retrieve all properties in one call using NumPy indexing
    return np.array([
        event_ids[idx_array],
        magnitudes[idx_array],
        depths[idx_array],
        X_coords[idx_array],
        Y_coords[idx_array],
        Z_coords[idx_array],
        dates[idx_array]
    ])


def get_sample_from_eid_numpy(df, event_id, radius=10, past_years=30, num_earthquakes=30, big_eq_min_magnitude=5.5):
    sample_of_eid, target_earthquake = space_time_filter_numpy(df, event_id, radius, past_years, num_earthquakes)
    properties = sample_of_eid[['xM', 'Depth(km)', 'X', 'Y', 'Z', 'Datetime']].values

    # Calculate differences between consecutive rows for all columns except Event ID
    differences = np.diff(properties, axis=0)

    # Extract datetime differences and calculate time differences in hours
    datetime_col = properties[:, 5]
    time_diffs_hours = np.diff(datetime_col).astype('timedelta64[s]').astype(float) / 3600.0

    differences[:, 5] = time_diffs_hours
    X_eid = differences

    # Determine y_eid: 1 if target earthquake magnitude >= big_eq_min_magnitude, otherwise 0
    y_eid = 1 if target_earthquake['xM'] >= big_eq_min_magnitude else 0
    return X_eid, y_eid


def get_aftershocks_from_eq_numpy(df, event_id, radius=10, big_eq_min_magnitude=5.5):
    event_mag = earthquake_filter_utils.get_value_from_eid(df, event_id, "xM")
    if event_mag < big_eq_min_magnitude:
        raise ValueError(
            f"Earthquake magnitude should be at least {big_eq_min_magnitude}. Given event_id={event_id}, xM={event_mag}")

    aftershock_duration_in_hours = 10 ** (event_mag - 3.0) * 24  ## FIXME: This might be wrong
    event_datetime = earthquake_filter_utils.get_value_from_eid(df, event_id, "Datetime")
    end_time = event_datetime + np.timedelta64(int(aftershock_duration_in_hours), 'h')
    datetimes = df['Datetime'].values
    latitudes = df['Latitude'].values
    longitudes = df['Longitude'].values

    event_lat = earthquake_filter_utils.get_value_from_eid(df, event_id, "Latitude")
    event_lon = earthquake_filter_utils.get_value_from_eid(df, event_id, "Longitude")

    distances = math_utils.haversine(event_lat, event_lon, latitudes, longitudes)
    distance_mask = distances <= radius

    time_mask = (datetimes > event_datetime) & (datetimes <= end_time)

    combined_mask = distance_mask & time_mask
    return df[combined_mask]


def remove_all_aftershocks_from_data_numpy(df, radius=10, big_eq_min_magnitude=5.5):
    # Create a copy of the original DataFrame to avoid modifying it
    df_copy = df.copy()

    # Filter large earthquakes based on the magnitude threshold
    df_large_eqs = df_copy[df_copy["xM"] >= big_eq_min_magnitude]

    # Create an empty mask for aftershocks
    aftershock_mask = np.zeros(len(df_copy), dtype=bool)

    # Convert 'Event ID' to a NumPy array for faster access
    event_ids = df_copy['Event ID'].values

    # Loop through each large earthquake and use the helper function to find aftershocks
    for event_id in df_large_eqs['Event ID']:
        # Use the helper function get_aftershocks_from_eq_numpy to find aftershocks
        aftershocks_df = get_aftershocks_from_eq_numpy(df_copy, event_id, radius, big_eq_min_magnitude)

        # Get the 'Event ID' values for the aftershocks and mark them in the mask
        aftershock_event_ids = aftershocks_df['Event ID'].values
        aftershock_mask |= np.isin(event_ids, aftershock_event_ids)

    # Use the aftershock mask to remove aftershocks from the copied DataFrame
    df_without_aftershocks = df_copy[~aftershock_mask]

    return df_without_aftershocks