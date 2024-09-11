import torch
import numpy as np
from src.util.earthquake_efficient_filter_utils import get_sample_from_eid_numpy


def create_classification_data_random(df, total_samples, radius=10, past_years=30, num_earthquakes=30,
                                      big_eq_min_magnitude=5.5):
    df = df.reset_index(drop=True)
    selected_indices = np.random.choice(df.index, total_samples, replace=False)

    X_samples = []
    y_samples = []
    for idx in selected_indices:
        event_id = df.loc[idx, 'Event ID']
        try:
            X_eid, y_eid, _ = get_sample_from_eid_numpy(df, event_id, radius, past_years, num_earthquakes,
                                                     big_eq_min_magnitude)

            X_samples.append(X_eid)
            y_samples.append(y_eid)
        except Exception as e:
            print(f"Error processing event ID {event_id}: {e}")
            continue

    X_np = np.array(X_samples, dtype=np.float32)
    y_np = np.array(y_samples, dtype=np.float32)

    X_tensor = torch.tensor(X_np, dtype=torch.float32)
    y_tensor = torch.tensor(y_np, dtype=torch.float32)

    return X_tensor, y_tensor


def create_classification_data(df, large_eq_df=None, radius=10, past_years=30, num_earthquakes=30, big_eq_min_magnitude=5.5, ):
    if large_eq_df is None:
        large_eq_df = df

    mag_eids = large_eq_df['Event ID']  # Assumed 'Event ID' column exists in test_df

    X_samples = []
    y_samples = []
    for eid in mag_eids:
        try:
            X_eid, y_eid = get_sample_from_eid_numpy(df, eid, radius, past_years, num_earthquakes, big_eq_min_magnitude)
            X_samples.append(X_eid)
            y_samples.append(y_eid)
        except Exception as e:
            print(f"Error processing event ID {eid}: {e}")
            continue

    X_np = np.array(X_samples, dtype=np.float32)
    y_np = np.array(y_samples, dtype=np.float32)

    X_tensor = torch.tensor(X_np, dtype=torch.float32)
    y_tensor = torch.tensor(y_np, dtype=torch.float32)
    return X_tensor, y_tensor
