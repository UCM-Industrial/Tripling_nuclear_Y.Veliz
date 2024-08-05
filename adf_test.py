import pandas as pd
from statsmodels.tsa.stattools import adfuller

def perform_adf_test(data):
    """
    This function performs the Augmented Dickey-Fuller (ADF) test on a given time series data.
    It checks if the data is stationary, i.e., its mean and variance do not change over time.

    Parameters:
    data (pandas.Series): The time series data to be tested.

    Returns:
    pandas.DataFrame: A DataFrame containing the ADF test results. If the input data is constant,
    the function returns a DataFrame with a single row containing 'No' in the 'Stationary' column
    and an error message in the 'Error' column.
    """
    if data.nunique().values[0] == 1:
        return pd.DataFrame([{
            'ADF Statistic': None,
            'p-value': None,
            'Num Lags': None,
            'Num Observations': None,
            '1%': None,
            '5%': None,
            '10%': None,
            'Stationary': 'No',
            'Error': 'Input data is constant'
        }])

    adf_result = adfuller(data)
    p_value = adf_result[1]
    stationary = 'Yes' if p_value <= 0.05 else 'No'
    
    result = {
        'ADF Statistic': adf_result[0],
        'p-value': p_value,
        'Num Lags': adf_result[2],
        'Num Observations': adf_result[3],
        '1%': adf_result[4]['1%'],
        '5%': adf_result[4]['5%'],
        '10%': adf_result[4]['10%'],
        'Stationary': stationary
    }

    return pd.DataFrame([result])
