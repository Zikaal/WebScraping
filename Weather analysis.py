import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import time

def get_weather_data():
    url = "https://weather.com/weather/today/l/a53972e14c64e70bca39cfe9ba0568d951b70605ca314dc9b3aeec8fac43acb6"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')

    temperature_f = soup.find('span', class_='TodayDetailsCard--feelsLikeTempValue--2icPt').text
    temperature_c = int((int(temperature_f[:-1]) - 32) * 5/9)

    humidity = soup.find('span', attrs={'data-testid': 'PercentageValue'}).text
    humidity = humidity.replace("%", "")

    wind = soup.find('span', class_='Wind--windWrapper--3Ly7c undefined').text
    wind = wind.replace("Wind Direction", "")
    wind_kmh = int(int(wind.split()[0]) * 1.60934)

    date = pd.to_datetime('now')

    return date, temperature_c, humidity, wind_kmh

try:
    weather_data = pd.read_csv('weather_data.csv', parse_dates=['Date'], index_col='Date')
except FileNotFoundError:
    weather_data = pd.DataFrame(columns=['Date', 'Temperature(°C)', 'Humidity', 'Wind(km/h)'])

while True:
    date, temperature_c, humidity, wind_kmh = get_weather_data()

    weather_data.loc[date] = {'Temperature(°C)': temperature_c, 'Humidity': humidity, 'Wind(km/h)': wind_kmh}

    weather_data.to_csv('weather_data.csv')

    plt.figure(figsize=(10, 6))

    weather_data['Temperature(°C)'] = pd.to_numeric(weather_data['Temperature(°C)'], errors='coerce')
    weather_data['Humidity'] = pd.to_numeric(weather_data['Humidity'], errors='coerce')
    weather_data['Wind(km/h)'] = pd.to_numeric(weather_data['Wind(km/h)'], errors='coerce')

    plt.plot(weather_data.index, weather_data['Temperature(°C)'], label='Temperature (°C)')
    plt.plot(weather_data.index, weather_data['Humidity'], label='Humidity')
    plt.plot(weather_data.index, weather_data['Wind(km/h)'], label='Wind (km/h)')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Weather Data')
    plt.legend()
    plt.grid(True)
    plt.show()

    time.sleep(1800)  
