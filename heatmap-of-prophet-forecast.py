#This script will create heatmaps for checkin and checkout forecasts using the Prophet model predictions. Note that the heatmaps are based on aggregated forecasted values, so they might not be as granular as the original heatmap.


import numpy as np

def prophet_forecast_to_heatmap(forecast, start_date, periods):
    # Extract week number and weekday from the forecast
    forecast['week'] = forecast['ds'].dt.isocalendar().week
    forecast['weekday'] = forecast['ds'].dt.weekday
    
    # Create a pivot table to aggregate forecasted values by week number and weekday
    pivot_table = forecast.pivot_table(index='weekday', columns='week', values='yhat', aggfunc=np.sum)
    
    return pivot_table

# Create heatmap for the checkin forecast
checkin_heatmap = prophet_forecast_to_heatmap(checkin_forecast, df['checkin'].min(), 365)
plt.figure(figsize=(12, 6))
ax = sns.heatmap(checkin_heatmap, cmap='YlGnBu', linewidths=0.5)
plt.title("Checkin Forecast Heatmap")
plt.xlabel("Week Number")
plt.ylabel("Weekday")
plt.yticks(range(7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.colorbar(ax.get_children()[0], ax=ax, orientation='horizontal', pad=0.07, label='Checkin Forecast Value')
plt.show()

# Create heatmap for the checkout forecast
checkout_heatmap = prophet_forecast_to_heatmap(checkout_forecast, df['checkout'].min(), 365)
plt.figure(figsize=(12, 6))
ax = sns.heatmap(checkout_heatmap, cmap='YlGnBu', linewidths=0.5)
plt.title("Checkout Forecast Heatmap")
plt.xlabel("Week Number")
plt.ylabel("Weekday")
plt.yticks(range(7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.colorbar(ax.get_children()[0], ax=ax, orientation='horizontal', pad=0.07, label='Checkout Forecast Value')
plt.show()
