import numpy as np
import pandas as pd


def calculate_gini(array: np.ndarray | pd.Series) -> float:
    """Calculate the Gini coefficient of an attention/ratings distribution."""
    arr = np.array(array, dtype=np.float64)
    if np.amin(arr) < 0:
        arr -= np.amin(arr)
    arr += 1e-7
    arr = np.sort(arr)
    n = arr.shape[0]
    index = np.arange(1, n + 1)
    return float(np.sum((2 * index - n - 1) * arr) / (n * np.sum(arr)))


def calculate_compatibility_lift(
    df: pd.DataFrame,
    iid_col: str = 'iid',
    pid_col: str = 'pid',
    decision_col: str = 'dec',
    match_col: str = 'match'
) -> dict[str, float]:
    """Calculate observed vs expected match rate under the independence assumption."""
    user_p_yes = df.groupby(iid_col)[decision_col].mean().to_dict()
    p_yes_i = df[iid_col].map(user_p_yes)
    p_yes_j = df[pid_col].map(user_p_yes)
    
    expected_match = p_yes_i * p_yes_j
    observed_rate = df[match_col].mean()
    expected_rate = expected_match.mean()
    lift = (observed_rate - expected_rate) / expected_rate
    
    return {
        'observed_match_rate': float(observed_rate),
        'expected_match_rate': float(expected_rate),
        'compatibility_lift': float(lift)
    }
