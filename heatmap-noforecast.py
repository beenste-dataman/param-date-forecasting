#This script first filters out rows with no checkin and checkout dates, then creates a frequency table for checkin and checkout dates. The table is then pivoted to create a format suitable for a heatmap. Finally, the seaborn library is used to create and display the heatmap.

#The resulting heatmap will display the number of visits (or popularity) for each day of the year. With the x-axis showing week of year.


import pandas as pd
from urllib.parse import urlparse, parse_qs
import seaborn as sns
import matplotlib.pyplot as plt

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

# Create a frequency table for checkin and checkout dates
date_range = pd.date_range(start=df['checkin'].min(), end=df['checkout'].max())
freq_table = pd.DataFrame(date_range, columns=['date'])
freq_table['checkin_count'] = 0
freq_table['checkout_count'] = 0

for _, row in df.iterrows():
    checkin_date = row['checkin']
    checkout_date = row['checkout']
    visits = row['Visits']

    freq_table.loc[freq_table['date'] == checkin_date, 'checkin_count'] += visits
    freq_table.loc[freq_table['date'] == checkout_date, 'checkout_count'] += visits

# Pivot the frequency table for heatmap
freq_table['weekday'] = freq_table['date'].dt.weekday
freq_table['week'] = freq_table['date'].dt.isocalendar().week
pivot_table = freq_table.pivot_table(index='weekday', columns='week', values='checkin_count', fill_value=0)

# Create heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(pivot_table, annot=True, fmt='d', cmap='YlGnBu', linewidths=0.5, cbar=False)
plt.title("Checkin Heatmap")
plt.xlabel("Week Number")
plt.ylabel("Weekday")
plt.yticks(range(7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.show()
