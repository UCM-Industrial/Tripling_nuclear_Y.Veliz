import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

def optimize_sarimax(series, p_range, d_range, q_range, seasonal_period, enable_seasonality):
    """
    This function optimizes the SARIMAX model parameters (p, d, q) and (P, D, Q, m) for a given time series.
    It iterates through different combinations of these parameters and selects the one that yields the lowest AIC (Akaike Information Criterion).

    Parameters:
    - series (pandas.Series): The time series data to be modeled.
    - p_range (list): A list of integers representing the range of p values to be tested.
    - d_range (list): A list of integers representing the range of d values to be tested.
    - q_range (list): A list of integers representing the range of q values to be tested.
    - seasonal_period (int): The number of periods in a season.
    - enable_seasonality (bool): A flag indicating whether to include seasonal components in the model.

    Returns:
    - best_aic (float): The lowest AIC value obtained during the optimization process.
    - best_order (tuple): The optimal (p, d, q) values that yield the lowest AIC.
    - best_seasonal_order (tuple): The optimal (P, D, Q, m) values that yield the lowest AIC.
    - best_mdl (statsmodels.tsa.statespace.sarimax.SARIMAX): The SARIMAX model object with the best parameters.
    """    
    best_aic = np.inf
    best_order = None
    best_seasonal_order = None
    best_mdl = None

    P = D = Q = range(2)
    m = seasonal_period

    for p in p_range:
        for d in d_range:
            for q in q_range:
                for P_ in P:
                    for D_ in D:
                        for Q_ in Q:
                            try:
                                temp_model = SARIMAX(series,
                                                     order=(p, d, q),
                                                     seasonal_order=(P_, D_, Q_, m) if enable_seasonality else (0, 0, 0, 0),
                                                     enforce_stationarity=False,
                                                     enforce_invertibility=False)
                                results = temp_model.fit(disp=False)
                                if results.aic < best_aic:
                                    best_aic = results.aic
                                    best_order = (p, d, q)
                                    best_seasonal_order = (P_, D_, Q_, m) if enable_seasonality else (0, 0, 0, 0)
                                    best_mdl = results
                            except:
                                continue
    return best_aic, best_order, best_seasonal_order, best_mdl

def optimize_sarimax_models(df, selected_countries, variable, p_range, d_range, q_range, seasonal_period, start_year, end_year, enable_seasonality):
    """
    This function optimizes SARIMAX models for multiple countries based on given parameters and time series data.

    Parameters:
    - df (pandas.DataFrame): The DataFrame containing the time series data.
    - selected_countries (list): A list of country names for which the models will be optimized.
    - variable (str): The name of the variable (column) in the DataFrame to be modeled.
    - p_range (list): A list of integers representing the range of p values to be tested for the SARIMAX model.
    - d_range (list): A list of integers representing the range of d values to be tested for the SARIMAX model.
    - q_range (list): A list of integers representing the range of q values to be tested for the SARIMAX model.
    - seasonal_period (int): The number of periods in a season.
    - start_year (int): The starting year for the time series data.
    - end_year (int): The ending year for the time series data.
    - enable_seasonality (bool): A flag indicating whether to include seasonal components in the SARIMAX model.

    Returns:
    - sarimax_results (dict): A dictionary containing the results of the SARIMAX model optimization for each country.
      The keys are country names, and the values are dictionaries with the following keys:
      - 'aic': The Akaike Information Criterion (AIC) value of the optimized model.
      - 'order': The optimal (p, d, q) values for the SARIMAX model.
      - 'seasonal_order': The optimal (P, D, Q, m) values for the SARIMAX model.
      - 'model_summary': The summary of the optimized SARIMAX model.
      - 'model_object': The optimized SARIMAX model object.
      If the model optimization fails or there is insufficient data for modeling, the value for the country will be a dictionary with the 'error' key.
    """    
    sarimax_results = {}

    for country in selected_countries:
        data_series = df[(df['Country'] == country) & 
                         (df['Date'] >= start_year) & 
                         (df['Date'] <= end_year) & 
                         (df[variable].notna())][variable]

        if data_series.empty or len(data_series) < max(p_range) + max(d_range) + max(q_range) + 1:
            sarimax_results[country] = {'error': 'Insufficient data for modeling.'}
            continue

        try:
            aic, order, seasonal_order, model = optimize_sarimax(data_series, p_range, d_range, q_range, seasonal_period, enable_seasonality)
            if model is not None:
                sarimax_results[country] = {
                    'aic': aic, 
                    'order': order, 
                    'seasonal_order': seasonal_order, 
                    'model_summary': model.summary(),
                    'model_object': model
                }
            else:
                sarimax_results[country] = {'error': 'Model optimization failed.'}
        except Exception as e:
            sarimax_results[country] = {'error': str(e)}

    return sarimax_results

def forecast_future(sarimax_results, df, variable, start_year, forecast_until_year=2100, replace_negative_forecast=False, sigma=2):
    """
    This function forecasts future values for a given variable using SARIMAX models.

    Parameters:
    - sarimax_results (dict): A dictionary containing the results of the SARIMAX model optimization for each country.
      The keys are country names, and the values are dictionaries with the 'model_object' key.
    - df (pandas.DataFrame): The DataFrame containing the time series data.
    - variable (str): The name of the variable (column) in the DataFrame to be forecasted.
    - start_year (int): The starting year for the time series data.
    - forecast_until_year (int): The year until which the forecasts will be made. Default is 2100.
    - replace_negative_forecast (bool): A flag indicating whether to replace negative forecast values with zero. Default is False.
    - sigma (float): The confidence interval for the forecasts. Default is 2.

    Returns:
    - forecast_results (dict): A dictionary containing the forecasted values and their confidence intervals for each country.
      The keys are forecast keys in the format "{country} ({forecast_until_year}) - SARIMAX {order} ({seasonal_order[3]})".
      The values are dictionaries with the following keys:
      - 'forecast_values': A pandas Series containing the forecasted values.
      - 'forecast_ci': A pandas DataFrame containing the lower and upper confidence interval bounds.
      - 'country': The country name.
      - 'model': The model used for forecasting, in this case, 'SARX'.
      - 'order': The order of the SARIMAX model.
      - 'seasonal_order': The seasonal order of the SARIMAX model.
      - 'forecast_until_year': The year until which the forecasts were made.
    """    
    forecast_results = {}

    for country, result in sarimax_results.items():
        if 'model_object' in result:
            filtered_data = df[(df['Country'] == country) & (df['Date'] >= start_year)]
            filtered_data = filtered_data.sort_values('Date')  
            last_data_year = filtered_data['Date'].max()

            if pd.isnull(last_data_year) or not isinstance(last_data_year, (int, np.integer)):
                raise ValueError(f"The last year of the filtered data is invalid: {last_data_year}")

            forecast_years = pd.date_range(start=pd.to_datetime(str(int(last_data_year) + 1)), end=pd.to_datetime(str(forecast_until_year + 1)), freq='YE').year
            steps_to_forecast_until = len(forecast_years)
            model = result['model_object']
            forecast = model.get_forecast(steps=steps_to_forecast_until)
            forecast_values = forecast.predicted_mean
            forecast_ci = forecast.conf_int(alpha=1 - (sigma/2))
            forecast_ci.columns = ['mean_ci_lower', 'mean_ci_upper']
            forecast_values.index = forecast_years
            forecast_ci.index = forecast_years

            last_value = filtered_data.iloc[-1][variable]
            forecast_values.iloc[0] = last_value

            if replace_negative_forecast:
                forecast_values[forecast_values < 0] = 0

            forecast_key = f"{country} ({forecast_until_year}) - SARIMAX {result['order']} ({result['seasonal_order'][3]})"
            forecast_results[forecast_key] = {
                'forecast_values': forecast_values,
                'forecast_ci': forecast_ci,
                'country': country,
                'model': 'SARX',
                'order': result['order'],
                'seasonal_order': result['seasonal_order'],
                'forecast_until_year': forecast_until_year
            }

    return forecast_results
