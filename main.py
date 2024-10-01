# import requests

# url = "https://acuityscheduling.com/api/v1/calendars"

# headers = {
#     "accept": "application/json",
#     "authorization": "Basic MTc2Njk0OTk6YWFiYTdhMjlkMzNhOGJhN2NiMjc1MGY2YmNkZjFkNGU="
# }

# response = requests.get(url, headers=headers)

# print(response.text)


import requests
import json
import pandas as pd
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(3)).strftime('%Y-%m-%d')

url = f'https://acuityscheduling.com/api/v1/appointments'

headers = {
    "accept": "application/json",
    "authorization": "Basic MTc2Njk0OTk6YWFiYTdhMjlkMzNhOGJhN2NiMjc1MGY2YmNkZjFkNGU="
}

params = {
    'minDate': yesterday,
    'maxDate': yesterday,
    'calendarID': 6735407
}
response = requests.get(url, headers=headers, params=params)
print(json.loads(response.content.decode('utf-8')))