from src.util.earthquake_filter_utils import get_value_from_eid
from src.util.math_utils import haversine
from src.util.math_utils import date_time_diff_in_hours

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