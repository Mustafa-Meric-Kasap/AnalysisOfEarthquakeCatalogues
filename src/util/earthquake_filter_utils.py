import src.util.math_utils as math_utils
from dateutil.relativedelta import relativedelta
import pandas as pd

def get_value_from_eid(df, event_id, column_name):
    # FIXME: Later add try exception block.
    value = df.loc[df['Event ID'] == event_id, column_name].values[0]
    return value

def distance_filter(df, event_id, radius_km=10):
    event_lat = get_value_from_eid(df, event_id, "Latitude")
    event_lon = get_value_from_eid(df, event_id,"Longitude")

    distances = df.apply(lambda eq: math_utils.haversine(event_lat, event_lon, eq['Latitude'], eq['Longitude']), axis=1)
    mask = distances <= radius_km
    filtered_df = df[mask].copy()
    return filtered_df


def magnitude_filter(df: pd.DataFrame, magnitude:float):
    df_copy = df.copy()
    filtered_df = df_copy[df_copy["xM"] >= magnitude]
    return filtered_df


def time_filter(df, event_id, years):
    event_datetime = get_value_from_eid(df, event_id, "Datetime")

    # Ensure the event_datetime is in pandas Timestamp format
    if isinstance(event_datetime, pd.Timestamp):
        event_datetime = pd.to_datetime(event_datetime)
    else:
        event_datetime = pd.to_datetime(str(event_datetime))

    cutoff_date = event_datetime - relativedelta(years=years)

    # Create a copy of the original DataFrame to avoid modifying it
    df_copy = df.copy()

    # Ensure the 'Datetime' column is in pandas datetime format
    df_copy['Datetime'] = pd.to_datetime(df_copy['Datetime'])

    filtered_df = df_copy[df_copy['Datetime'] >= cutoff_date]
    return filtered_df


def past_earthquakes_filter(df, event_id, num_earthquakes=30):
    # Get the datetime for the event using the event ID
    event_datetime = get_value_from_eid(df, event_id, "Datetime")

    # Ensure the event_datetime is in pandas Timestamp format
    if isinstance(event_datetime, pd.Timestamp):
        event_datetime = pd.to_datetime(event_datetime)
    else:
        event_datetime = pd.to_datetime(str(event_datetime))

    df_copy = df.copy()

    # Ensure the 'Datetime' column is in pandas datetime format
    df_copy['Datetime'] = pd.to_datetime(df_copy['Datetime'])

    # Filter past earthquakes
    past_earthquakes = df_copy[df_copy['Datetime'] < event_datetime]
    past_earthquakes_sorted = past_earthquakes.sort_values(by='Datetime', ascending=False)
    filtered_df = past_earthquakes_sorted.head(num_earthquakes)

    # Reverse the order of filtered_df
    filtered_df = filtered_df.iloc[::-1]

    # Get the row corresponding to the event ID
    event_row = df_copy[df_copy['Event ID'] == event_id]

    # Concatenate the past earthquakes and the event row
    result = pd.concat([filtered_df, event_row], ignore_index=True)

    return result
