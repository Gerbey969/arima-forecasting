import requests
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from datetime import date, timedelta

# Отримання даних за кожен день протягом останніх 30 днів
base_url = "https://api.privatbank.ua/p24api/exchange_rates?json&date="
end_date = date.today() - timedelta(days=1)  # Отримання дати 30 днів тому
start_date = end_date - timedelta(days=29)  # Отримання початкової дати
currency_data = []

current_date = start_date
while current_date <= end_date:
    formatted_date = current_date.strftime("%d.%m.%Y")
    url = base_url + formatted_date
    response = requests.get(url)
    data = response.json()
    currency_data.append(data)
    current_date += timedelta(days=1)

# Обробка даних
usd_exchange_rates = []
for data in currency_data:
    exchange_rates = data["exchangeRate"]
    for rate in exchange_rates:
        if rate["currency"] == "EUR":
            usd_exchange_rates.append({
                "date": data["date"],
                "saleRate": float(rate["saleRate"]),
                "purchaseRate": float(rate["purchaseRate"])
            })

df = pd.DataFrame(usd_exchange_rates)
df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")

print(df)

# Побудова ARIMA моделі
model = ARIMA(df["saleRate"], order=(1, 1, 1))
model_fit = model.fit()

# Прогнозування
forecast = model_fit.forecast(steps=7)  # Прогноз на 7 днів вперед

# Виведення прогнозу
print("ARIMA Forecast:")
print(forecast)
