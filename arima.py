import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def optimize_arima(series, p_range, d_range, q_range):
    """
    This function optimizes the parameters of an ARIMA model for a given time series.

    Parameters:
    series (pandas.Series): The time series data to be modeled.
    p_range (list): A list of integers representing the range of p (AR order) values to be tested.
    d_range (list): A list of integers representing the range of d (differencing order) values to be tested.
    q_range (list): A list of integers representing the range of q (MA order) values to be tested.

    Returns:
    tuple: A tuple containing the best AIC value, the corresponding order (p, d, q), and the ARIMA model object with the best AIC.
    """    
    best_aic = np.inf
    best_order = None
    best_mdl = None

    for p in p_range:
        for d in d_range:
            for q in q_range:
                try:
                    temp_model = ARIMA(series, order=(p, d, q))
                    results = temp_model.fit()
                    if results.aic < best_aic:
                        best_aic = results.aic
                        best_order = (p, d, q)
                        best_mdl = results
                except:
                    continue
    return best_aic, best_order, best_mdl

def optimize_arima_models(df, selected_countries, variable, p_range, d_range, q_range, start_year, end_year):
    """
    This function optimizes ARIMA models for a given set of countries and time series data.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the time series data.
    selected_countries (list): A list of country names for which the models will be optimized.
    variable (str): The name of the variable (column) in the DataFrame to be modeled.
    p_range (list): A list of integers representing the range of p (AR order) values to be tested.
    d_range (list): A list of integers representing the range of d (differencing order) values to be tested.
    q_range (list): A list of integers representing the range of q (MA order) values to be tested.
    start_year (int): The starting year for the time series data.
    end_year (int): The ending year for the time series data.

    Returns:
    dict: A dictionary containing the results of the ARIMA model optimization for each country.
          The keys are country names, and the values are dictionaries containing the AIC, order, model summary,
          and model object (if successful), or an error message (if unsuccessful).
    """
    arima_results = {}

    for country in selected_countries:
        data_series = df[(df['Country'] == country) & 
                         (df['Date'] >= start_year) & 
                         (df['Date'] <= end_year) & 
                         (df[variable].notna())][variable]

        if data_series.empty or len(data_series) < max(p_range) + max(d_range) + max(q_range) + 1:
            arima_results[country] = {'error': 'Insufficient data for modeling.'}
            continue

        try:
            aic, order, model = optimize_arima(data_series, p_range, d_range, q_range)
            if model is not None:
                arima_results[country] = {
                    'aic': aic,
                    'order': order,
                    'model_summary': model.summary(),
                    'model_object': model
                }
            else:
                arima_results[country] = {'error': 'Model optimization failed.'}
        except Exception as e:
            arima_results[country] = {'error': str(e)}

    return arima_results

def forecast_future(arima_results, df, variable, start_year, forecast_until_year=2100, replace_negative_forecast=False, sigma=2):
    """
    This function forecasts future values using ARIMA models based on the provided results.

    Parameters:
    arima_results (dict): A dictionary containing the results of ARIMA model optimization for each country.
                          The keys are country names, and the values are dictionaries containing the AIC, order,
                          model summary, and model object (if successful), or an error message (if unsuccessful).
    df (pandas.DataFrame): The DataFrame containing the time series data.
    variable (str): The name of the variable (column) in the DataFrame to be forecasted.
    start_year (int): The starting year for the time series data.
    forecast_until_year (int): The year until which the forecasts will be made. Default is 2100.
    replace_negative_forecast (bool): A flag indicating whether negative forecast values should be replaced with zero. Default is False.
    sigma (float): The confidence interval multiplier for the forecast. Default is 2.

    Returns:
    dict: A dictionary containing the forecasted values, confidence intervals, country, model, order, and forecast until year
          for each country. The keys are forecast keys in the format "{country} ({forecast_until_year}) - ARIMA {order}".
    """
    forecast_results = {}

    for country, result in arima_results.items():
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

            forecast_key = f"{country} ({forecast_until_year}) - ARIMA {result['order']}"
            forecast_results[forecast_key] = {
                'forecast_values': forecast_values,
                'forecast_ci': forecast_ci,
                'country': country,
                'model': 'AR',
                'order': result['order'],
                'forecast_until_year': forecast_until_year
            }

    return forecast_results