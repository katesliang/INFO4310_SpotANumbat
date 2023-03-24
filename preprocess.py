import csv
from os import environ 
import pandas as pd
import requests

FILE_NAME = "numbats.csv"

def preprocess(file_name):
    df = pd.read_csv(file_name)
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        new_series = []
        for row in reader:
            if row["day"] != "NA":
                q = str(row["decimalLatitude"]) + ',' + str(row["decimalLongitude"])
                params = {
                    "key": environ.get("API_KEY"),
                    "q": q,
                    "dt": row["day"]
                }
                response = requests.get("http://api.weatherapi.com/v1/history.json", params=params)
                if response.status_code == 200:
                    condition = response.json()["forecast"]["forecastday"][0]["day"]["condition"]["text"]  
                    new_series.append(condition)
                else:
                    new_series.append("")
            else:
                new_series.append("")
        new_column = pd.DataFrame({"WeatherCondition": pd.Series(new_series)})
        df = df.merge(new_column, left_index = True, right_index = True)
    df.to_csv("data.csv", index = False)
    
preprocess(FILE_NAME)

