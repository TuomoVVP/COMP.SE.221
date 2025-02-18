import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# API Keys and Endpoints
ELECTRICITY_PRICE_API_URL = "https://transparency.entsoe.eu/api"
OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/forecast"
OPENWEATHERMAP_API_KEY = "your_openweathermap_api_key"

# Function to fetch electricity price data
def fetch_electricity_prices(start_date, end_date):
    params = {
        "documentType": "A44",
        "in_Domain": "10YFI-1--------U",
        "out_Domain": "10YFI-1--------U",
        "periodStart": start_date,
        "periodEnd": end_date,
        "securityToken": "your_entsoe_api_key"
    }
    response = requests.get(ELECTRICITY_PRICE_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch electricity price data")
        return None

# Function to fetch wind power generation data
def fetch_wind_power_data(lat, lon, start_date, end_date):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHERMAP_API_KEY,
        "start": start_date,
        "end": end_date
    }
    response = requests.get(OPENWEATHERMAP_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch wind power data")
        return None

# Function to parse and combine data
def combine_data(electricity_data, wind_data):
    # Parse electricity data
    electricity_df = pd.DataFrame(electricity_data['periods'])
    electricity_df['start_time'] = pd.to_datetime(electricity_df['start_time'])
    electricity_df.set_index('start_time', inplace=True)

    # Parse wind data
    wind_df = pd.DataFrame(wind_data['list'])
    wind_df['dt'] = pd.to_datetime(wind_df['dt'], unit='s')
    wind_df.set_index('dt', inplace=True)

    # Combine data
    combined_df = pd.merge_asof(electricity_df, wind_df, left_index=True, right_index=True)
    return combined_df

# Function to calculate correlation
def calculate_correlation(combined_df):
    correlation = combined_df['price'].corr(combined_df['wind.speed'])
    return correlation

# Main function
def main():
    # Define time range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Fetch data
    electricity_data = fetch_electricity_prices(start_date.strftime('%Y%m%d%H%M'), end_date.strftime('%Y%m%d%H%M'))
    wind_data = fetch_wind_power_data(60.1699, 24.9384, start_date.timestamp(), end_date.timestamp())

    if electricity_data and wind_data:
        combined_df = combine_data(electricity_data, wind_data)
        correlation = calculate_correlation(combined_df)
        print(f"Correlation between electricity price and wind power generation: {correlation}")
    else:
        print("Data fetching failed")

if __name__ == "__main__":
    main()