# Starting the required libraries
import numpy as np
import geopandas as gpd
import pandas as pd
from functools import reduce

# Part 1 : Preparing the data# 1.1 Downloading csv into dataframe
df_confirmed = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
df_deaths = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
df_recovered = pd.read_csv(
    'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')

df_confirmed.head(5)

# 1.2 Tidying the data
# Using melt() command in pandas (similar to gather() in R's tidyr)id_list = df_confirmed.columns.to_list()[:4]
vars_list = df_confirmed.columns.to_list()[4:]confirmed_tidy = pd.melt(df_confirmed, id_vars=id_list,
                                                                       value_vars=vars_list, var_name='Date', value_name='Confirmed')
deaths_tidy = pd.melt(df_deaths, id_vars=id_list,
                      value_vars=vars_list, var_name='Date', value_name='Deaths')
recovered_tidy = pd.melt(df_recovered, id_vars=id_list,
                         value_vars=vars_list, var_name='Date', value_name='recovered')  # 1.3 Merging the three dataframes into one
data_frames = [confirmed_tidy, deaths_tidy, recovered_tidy]
# 1.4 Each row should only represent one observation
df_corona = reduce(lambda left, right: pd.merge(
    left, right, on=id_list+['Date'], how='outer'), data_frames)
id_vars = df_corona.columns[:5]
data_type = ['Confirmed', 'Deaths', 'recovered']
df_corona = pd.melt(df_corona, id_vars=id_vars,
                    value_vars=data_type, var_name='type', value_name='Count')
df_corona['Date'] = pd.to_datetime(df_corona['Date'],
                                   format='%m/%d/%y', errors='raise')

df_corona.head(5)
