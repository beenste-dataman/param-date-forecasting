#Run this after to forecast checkin and checkout dates. 


import pandas as pd
from urllib.parse import urlparse, parse_qs
from prophet import Prophet

# Function to extract 'checkin' and 'checkout' parameters from a URL
def extract_params(url, param_name):
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    return params.get(param_name, [None])[0]

# DataFrame from the previous example
data = {'URL': ['https://example1.com/hotel?checkin=2023-04-01&checkout=2023-04-10',
                'https://example2.com/hotel?checkin=2023-04-05&checkout=2023-04-15',
                'https://example3.com/hotel'],
        'Visits': [150, 230, 120]}
df = pd.DataFrame(data)

# Extract 'checkin' and 'checkout' parameters and add them as new columns in the DataFrame
df['checkin'] = df['URL'].apply(lambda x: extract_params(x, 'checkin'))
df['checkout'] = df['URL'].apply(lambda x: extract_params(x, 'checkout'))

# Filter out rows with no checkin and checkout dates
df = df[df['checkin'].notnull() & df['checkout'].notnull()]

# Convert checkin and checkout dates to datetime objects
df['checkin'] = pd.to_datetime(df['checkin'])
df['checkout'] = pd.to_datetime(df['checkout'])

# Function to create and fit a Prophet model, then forecast the future dates
def forecast_dates(dates, visits, future_periods):
    freq_table = pd.DataFrame({'date': dates, 'visits': visits})
    prophet_data = freq_table[['date', 'visits']].rename(columns={'date': 'ds', 'visits': 'y'})
    model = Prophet()
    model.fit(prophet_data)
    future_dates = model.make_future_dataframe(periods=future_periods, freq='D')
    forecast = model.predict(future_dates)
    return model, forecast

# Forecast checkin dates
checkin_model, checkin_forecast = forecast_dates(df['checkin'], df['Visits'], 365)

# Forecast checkout dates
checkout_model, checkout_forecast = forecast_dates(df['checkout'], df['Visits'], 365)

# Plot the checkin and checkout forecasts
fig1 = checkin_model.plot(checkin_forecast)
plt.title("Checkin Forecast")
plt.show()

fig2 = checkout_model.plot(checkout_forecast)
plt.title("Checkout Forecast")
plt.show()
