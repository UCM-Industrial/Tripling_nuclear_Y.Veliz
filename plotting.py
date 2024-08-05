import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_historical_data(df, selected_countries, variable, start_year, end_year, ax):
    """
    This function plots historical data for a given variable and selected countries.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the historical data. It should have columns 'Country', 'Date', and the variable to be plotted.
    selected_countries (list): A list of country names for which the data needs to be plotted.
    variable (str): The variable to be plotted (e.g., 'Solar', 'Wind', 'Hydro').
    start_year (int): The starting year for the plot.
    end_year (int): The ending year for the plot.
    ax (matplotlib.axes.Axes): The Axes object on which the plot will be drawn.

    Returns:
    float: The maximum value of the plotted variable.
    """
    max_value = -float('inf')
    for country in selected_countries:
        country_data = df[(df['Country'] == country) & (df['Date'] >= start_year) & (df['Date'] <= end_year)]
        if not country_data.empty:
            max_value = max(max_value, country_data[variable].max())
            ax.plot(country_data['Date'], country_data[variable], label=country)
            
    ax.set_xlim([start_year, end_year])
    ax.set_ylim([0, max_value * 1.01])
    ax.legend()
    ax.set_title(f"{variable} Production (Historical)", fontsize=16, fontweight='bold')
    ax.set_ylabel('Production', fontsize=14)
    ax.set_xlabel('Year', fontsize=14)
    ax.grid(True, linestyle='--', which='both', color='grey', alpha=0.5)
    return max_value

def plot_historical_data_bar(df, selected_countries, variable, start_year, end_year, ax):
    """
    This function plots historical data for a given variable and selected countries using a bar chart.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the historical data. It should have columns 'Country', 'Date', and the variable to be plotted.
    selected_countries (list): A list of country names for which the data needs to be plotted.
    variable (str): The variable to be plotted (e.g., 'Solar', 'Wind', 'Hydro').
    start_year (int): The starting year for the plot.
    end_year (int): The ending year for the plot.
    ax (matplotlib.axes.Axes): The Axes object on which the plot will be drawn.

    Returns:
    float: The maximum value of the plotted variable.
    """
    combined_data = pd.DataFrame()

    for country in selected_countries:
        country_data = df[(df['Country'] == country) & (df['Date'] >= start_year) & (df['Date'] <= end_year)]
        if not country_data.empty:
            combined_data[country] = country_data.set_index('Date')[variable]

    combined_data = combined_data.fillna(0)
    bottom = pd.Series([0] * len(combined_data.index), index=combined_data.index)
    colors = plt.cm.tab20(np.linspace(0, 1, len(selected_countries)))
    max_value = combined_data.sum(axis=1).max()

    for i, country in enumerate(selected_countries):
        ax.bar(combined_data.index, combined_data[country], bottom=bottom, color=colors[i], label=country)
        bottom += combined_data[country]

    ax.set_xlim([start_year, end_year])
    ax.set_ylim([0, max_value * 1.01])
    ax.legend()
    ax.set_title(f"{variable} Production (Historical)", fontsize=16, fontweight='bold')
    ax.set_ylabel('Production', fontsize=14)
    ax.set_xlabel('Year', fontsize=14)
    ax.grid(True, linestyle='--', which='both', color='grey', alpha=0.5)
    return max_value

def plot_historical_data_stacked_area(df, selected_countries, variable, start_year, end_year, ax):
    """
    This function plots historical data for a given variable and selected countries using a stacked area chart.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the historical data. It should have columns 'Country', 'Date', and the variable to be plotted.
    selected_countries (list): A list of country names for which the data needs to be plotted.
    variable (str): The variable to be plotted (e.g., 'Solar', 'Wind', 'Hydro').
    start_year (int): The starting year for the plot.
    end_year (int): The ending year for the plot.
    ax (matplotlib.axes.Axes): The Axes object on which the plot will be drawn.

    Returns:
    float: The maximum value of the plotted variable.
    """    
    combined_data = pd.DataFrame()

    for country in selected_countries:
        country_data = df[(df['Country'] == country) & (df['Date'] >= start_year) & (df['Date'] <= end_year)]
        if not country_data.empty:
            combined_data[country] = country_data.set_index('Date')[variable]

    combined_data = combined_data.fillna(0)

    ax.stackplot(combined_data.index, combined_data.T, labels=combined_data.columns, alpha=0.8)
    max_value = combined_data.sum(axis=1).max()

    ax.set_xlim([start_year, end_year])
    ax.set_ylim([0, max_value * 1.01])
    ax.legend()
    ax.set_title(f"{variable} Production (Historical)", fontsize=16, fontweight='bold')
    ax.set_ylabel('Production', fontsize=14)
    ax.set_xlabel('Year', fontsize=14)
    ax.grid(True, linestyle='--', which='both', color='grey', alpha=0.5)
    return max_value

def plot_data(df, forecast_results, forecast_keys, variable, plot_type, ax, show_confidence_interval=False):
    """
    This function plots historical and forecasted data for a given variable and selected countries.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the historical data. It should have columns 'Country', 'Date', and the variable to be plotted.
    forecast_results (dict): A dictionary containing forecast results for each country. Each entry should have keys 'country', 'forecast_values', 'forecast_until_year', and optionally 'forecast_ci'.
    forecast_keys (list): A list of keys identifying the countries for which forecast results are available in the forecast_results dictionary.
    variable (str): The variable to be plotted (e.g., 'Solar', 'Wind', 'Hydro').
    plot_type (str): The type of plot to be generated. It can be one of 'Historical', 'Forecast', 'Both'.
    ax (matplotlib.axes.Axes): The Axes object on which the plot will be drawn.
    show_confidence_interval (bool, optional): If True, confidence intervals for the forecasted data will be plotted. Defaults to False.

    Returns:
    float: The maximum value of the plotted variable.
    """    
    combined_data = pd.DataFrame()

    for forecast_key in forecast_keys:
        forecast = forecast_results[forecast_key]
        country = forecast['country']
        historical_data = df[df['Country'] == country][['Date', variable]].set_index('Date')
        forecast_values = forecast['forecast_values'] if plot_type != "Historical" else None
        forecast_ci = forecast['forecast_ci'] if show_confidence_interval else None

        temp_combined_data = pd.DataFrame(index=range(int(historical_data.index.min()), forecast['forecast_until_year'] + 1))
        if plot_type == "Historical" or plot_type == "Both":
            temp_combined_data.loc[historical_data.index, variable] = historical_data[variable]

        if forecast_values is not None and (plot_type == "Forecast" or plot_type == "Both"):
            temp_combined_data.loc[forecast_values.index, variable] = forecast_values.values

        combined_data[country] = temp_combined_data[variable]

        if show_confidence_interval and forecast_ci is not None:
            ax.fill_between(forecast_ci.index, forecast_ci['mean_ci_lower'], forecast_ci['mean_ci_upper'], alpha=0.2, label=f'{country} Confidence Interval')

    combined_data = combined_data.dropna(how='all')
    max_value = combined_data.max().max()

    for forecast_key in forecast_keys:
        forecast = forecast_results[forecast_key]
        ax.plot(combined_data.index, combined_data[forecast['country']], label=forecast['country'])

    ax.set_title(f'{variable} Production ({plot_type})', fontsize=16, fontweight='bold')
    ax.set_ylabel('Production (TWh)', fontsize=14)
    ax.set_xlabel('Year', fontsize=14)
    ax.legend()
    ax.grid(True, linestyle='--', which='both', color='grey', alpha=0.5)
    ax.set_ylim(bottom=0)

    return max_value

def plot_data_stacked_bar(df, forecast_results, forecast_keys, variable, plot_type, ax):
    """
    This function plots historical and forecasted data for a given variable and selected countries using a stacked bar chart.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the historical data. It should have columns 'Country', 'Date', and the variable to be plotted.
    forecast_results (dict): A dictionary containing forecast results for each country. Each entry should have keys 'country', 'forecast_values', 'forecast_until_year'.
    forecast_keys (list): A list of keys identifying the countries for which forecast results are available in the forecast_results dictionary.
    variable (str): The variable to be plotted (e.g., 'Solar', 'Wind', 'Hydro').
    plot_type (str): The type of plot to be generated. It can be one of 'Historical', 'Forecast', 'Both'.
    ax (matplotlib.axes.Axes): The Axes object on which the plot will be drawn.

    Returns:
    float: The maximum value of the plotted variable.
    """
    combined_data = pd.DataFrame()

    for forecast_key in forecast_keys:
        forecast = forecast_results[forecast_key]
        country = forecast['country']
        historical_data = df[df['Country'] == country][['Date', variable]].set_index('Date')
        forecast_values = forecast['forecast_values'] if plot_type != "Historical" else None

        temp_combined_data = pd.DataFrame(index=range(int(historical_data.index.min()), forecast['forecast_until_year'] + 1))
        if plot_type == "Historical" or plot_type == "Both":
            temp_combined_data.loc[historical_data.index, variable] = historical_data[variable]

        if forecast_values is not None and (plot_type == "Forecast" or plot_type == "Both"):
            temp_combined_data.loc[forecast_values.index, variable] = forecast_values.values

        combined_data[country] = temp_combined_data[variable]

    combined_data = combined_data.fillna(0)

    ax.clear()

    bottom = pd.Series([0] * len(combined_data.index), index=combined_data.index)
    colors = plt.cm.tab20(np.linspace(0, 1, len(forecast_keys)))
    max_value = combined_data.sum(axis=1).max()

    for i, forecast_key in enumerate(forecast_keys):
        country = forecast_results[forecast_key]['country']
        ax.bar(combined_data.index, combined_data[country], bottom=bottom, color=colors[i], label=country)
        bottom += combined_data[country]

    ax.set_title(f'{variable} Production ({plot_type})', fontsize=16, fontweight='bold')
    ax.set_ylabel('Production (TWh)', fontsize=14)
    ax.set_xlabel('Year', fontsize=14)
    ax.legend()
    ax.grid(True, linestyle='--', which='both', color='grey', alpha=0.5)
    ax.set_ylim(bottom=0)

    return max_value

def plot_data_stacked_area(df, forecast_results, forecast_keys, variable, plot_type, ax):
    """
    This function plots historical and forecasted data for a given variable and selected countries using a stacked area chart.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the historical data. It should have columns 'Country', 'Date', and the variable to be plotted.
    forecast_results (dict): A dictionary containing forecast results for each country. Each entry should have keys 'country', 'forecast_values', 'forecast_until_year'.
    forecast_keys (list): A list of keys identifying the countries for which forecast results are available in the forecast_results dictionary.
    variable (str): The variable to be plotted (e.g., 'Solar', 'Wind', 'Hydro').
    plot_type (str): The type of plot to be generated. It can be one of 'Historical', 'Forecast', 'Both'.
    ax (matplotlib.axes.Axes): The Axes object on which the plot will be drawn.

    Returns:
    float: The maximum value of the plotted variable.
    """    
    combined_data = pd.DataFrame()

    for forecast_key in forecast_keys:
        forecast = forecast_results[forecast_key]
        country = forecast['country']
        historical_data = df[df['Country'] == country][['Date', variable]].set_index('Date')
        forecast_values = forecast['forecast_values'] if plot_type != "Historical" else None

        temp_combined_data = pd.DataFrame(index=range(int(historical_data.index.min()), forecast['forecast_until_year'] + 1))
        if plot_type == "Historical" or plot_type == "Both":
            temp_combined_data.loc[historical_data.index, variable] = historical_data[variable]

        if forecast_values is not None and (plot_type == "Forecast" or plot_type == "Both"):
            temp_combined_data.loc[forecast_values.index, variable] = forecast_values.values

        combined_data[country] = temp_combined_data[variable]

    combined_data = combined_data.fillna(0)

    ax.stackplot(combined_data.index, combined_data.T, labels=combined_data.columns, alpha=0.8)

    ax.set_title(f'{variable} Production ({plot_type})', fontsize=16, fontweight='bold')
    ax.set_ylabel('Production (TWh)', fontsize=14)
    ax.set_xlabel('Year', fontsize=14)
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='--', which='both', color='grey', alpha=0.5)
    ax.set_ylim(bottom=0)

    return combined_data.max().max()
