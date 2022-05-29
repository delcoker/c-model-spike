import pandas as pd
import datetime as dt

from google_sheets_picklist_values import get_pick_lists
from util import get_month_name, get_month_number
import numpy as np
from sklearn import linear_model
# from fbprophet import Prophet
from dateutil.relativedelta import relativedelta

pd.options.mode.chained_assignment = None  # default='warn'

# constants
logged_in = False
current_year = dt.date.today().year
number_of_years_data = 2
fiscal_start_year = 'January'
selected_product = 'Product 1'
desired_growth = 1
products = ['Product 1', 'Product 2', 'Product 3']
picklist_values = get_pick_lists
raw_data_sheet = "Sheet8"

# Import excel file
client_data = pd.read_excel("CMODEL NEW TEST.xlsx", sheet_name=raw_data_sheet)

client_data["Close Date"] = pd.to_datetime(client_data["Close Date"])

# Filter out data to be two years worth of data from current year
client_data_for_two_years = client_data[client_data["Close Date"].dt.year >= (current_year - number_of_years_data)]  # filter for 2 years

# Filter out the columns you need
filtered_data_for_calculation = client_data_for_two_years[["Product Name", "Close Date", "Stage", "ARR"]]

# Filter stage column to get "Closed Won"
data_just_for_closed_won = filtered_data_for_calculation[filtered_data_for_calculation["Stage"] == "Closed Won"]

# Create 'Close Year' column
data_just_for_closed_won["Close Year"] = data_just_for_closed_won["Close Date"].dt.year.apply(lambda x: (x - current_year) + (number_of_years_data + 1))  # Create 'Close Year' column
data_just_for_closed_won["Close Month"] = data_just_for_closed_won["Close Date"].dt.month

fiscal_start_year_number = get_month_number(fiscal_start_year)
fiscal_end_year = get_month_name(fiscal_start_year_number - 1)
freq = 'Q-' + fiscal_end_year.upper()

data_just_for_closed_won['Close Quarter'] = pd.PeriodIndex(data_just_for_closed_won['Close Date'], freq=freq).strftime('Q%q')


def select_product(product):
    # print(product)
    # Product Forecasts
    data_for_time_series = data_just_for_closed_won[['Close Date', 'ARR', 'Product Name']][data_just_for_closed_won['Product Name'] == product]
    # data_for_time_series['Close Month'] = data_for_time_series['Close Date'].dt.to_period('M')
    data_for_time_series['Close Month'] = data_for_time_series['Close Date'].dt.strftime('%m-%Y')

    summed_data = data_for_time_series.groupby(['Close Month'])['ARR'].sum().reset_index()
    summed_data['time'] = np.arange(len(summed_data.index))

    return summed_data, data_for_time_series


def run_linear_regression(product, summed_data):
    # Linear regression
    x = summed_data.time.values.reshape(-1, 1)
    y = summed_data['ARR'].values

    # fit the model
    model = linear_model.LinearRegression().fit(x, y)
    linear_model.LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)

    linear_predictions = model.predict([[1], [2], [3], [4], [5], [6]])

    return linear_predictions


'''
# Prophet

prophet_summed_data = summed_data.copy()[['Close Month', 'ARR']]
prophet_summed_data.columns = ['ds', 'y']
prophet_summed_data['ds'] = prophet_summed_data['ds'].astype(str)
prophet_summed_data['ds'] = pd.to_datetime(prophet_summed_data['ds'])
prophet_summed_data.head()


# fit model
model = Prophet()
model.fit(prophet_summed_data)

# define the period for which we want a prediction
future = list()
for i in range(1, 13):
    date = current_year - 1 + '-%02d' % i
    future.append([date])
future = pd.DataFrame(future)
future.columns = ['ds']
future['ds'] = pd.to_datetime(future['ds'])

# use the model to make a test forecast
forecast = model.predict(future)

# define the period for which we want a prediction
future = list()
for i in range(1, 13):
    date = current_year + '-%02d' % i
    future.append([date])
future = pd.DataFrame(future)
future.columns = ['ds']
future['ds'] = pd.to_datetime(future['ds'])
# use the model to make a forecast
forecast = model.predict(future)
# summarize the forecast
# print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())
# # plot forecast
# model.plot(forecast)
# pyplot.show()

'''


# C-MODEL
def run_c_model(product):
    # print('desired_growth', desired_growth, product)
    summed_data, data_for_time_series = select_product(product)

    # print(summed_data)
    c_model_summed_data = data_for_time_series.groupby(['Close Month'])['ARR'].sum().reset_index()

    last_month = (c_model_summed_data['Close Month'].iat[-1])
    last_month = dt.datetime.strptime(last_month, "%m-%Y")

    forecast_months_list = list()
    for i in range(1, 13):
        date = last_month + relativedelta(months=+i)
        forecast_months_list.append([date])

    forecast_months = pd.DataFrame(forecast_months_list)
    forecast_months.columns = ['Forecast Month']
    forecast_months['month'] = forecast_months['Forecast Month'].dt.month
    # print(forecast_months.head())

    # year totals
    summed_data_yearly_total = summed_data.copy()
    summed_data_yearly_total['year'] = pd.to_datetime(summed_data_yearly_total['Close Month']).dt.year
    summed_data_yearly_total = summed_data_yearly_total.groupby(['year'])['ARR'].sum().reset_index(name='sum ARR')
    # print(summed_data_yearly_total)

    # for each forecasted month get median( months total / year total)
    summed_data_monthly_average = summed_data.copy()
    summed_data_monthly_average['year'] = pd.to_datetime(summed_data_monthly_average['Close Month']).dt.year
    summed_data_monthly_average = pd.merge(summed_data_monthly_average, summed_data_yearly_total, how="inner", on=["year"])
    summed_data_monthly_average['year month average'] = summed_data_monthly_average['ARR'] / summed_data_monthly_average['sum ARR']
    summed_data_monthly_average['month'] = pd.to_datetime(summed_data_monthly_average['Close Month']).dt.month
    summed_data_monthly_average = summed_data_monthly_average.groupby('month')['year month average'].median().reset_index(name='median ARR')

    # average year 1 and year 2
    # get sum of grouped month values for year 1 and year 2
    summed_data_months = summed_data.copy()
    summed_data_months['month'] = pd.to_datetime(summed_data_months['Close Month']).dt.month
    summed_data_months = summed_data_months.groupby(['month'])['ARR'].mean().reset_index(name='mean ARR')

    # desired growth input
    final_forecast = summed_data_monthly_average.copy()
    final_forecast['median ARR x desired_growth'] = final_forecast['median ARR'] * desired_growth
    final_forecast = pd.merge(final_forecast, summed_data_months, how="inner", on=["month"])
    final_forecast['c-model'] = final_forecast['median ARR x desired_growth'] + final_forecast['mean ARR']
    # final_forecast

    # print(final_forecast)

    return final_forecast
