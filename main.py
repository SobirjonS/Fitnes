import requests
import json


# Example API request for appointments
def get_trial_sessions(date, calendar_id):
    url = f'https://acuityscheduling.com/api/v1/appointments'
    params = {
        'minDate': date,
        'maxDate': date,
        'calendarID': calendar_id
    }
    response = requests.get(url, headers=headers, params=params)
    return  response.content

    
# Request headers
url = "https://acuityscheduling.com/api/v1/calendars"

headers = {
    "accept": "application/json",
    "authorization": "Basic MTc2Njk0OTk6YWFiYTdhMjlkMzNhOGJhN2NiMjc1MGY2YmNkZjFkNGU="
}

response = requests.get(url, headers=headers)

data = response.content

decoded_data = data.decode('utf-8')

parsed_data = json.loads(decoded_data)

date = '2023-05-09'
for entry in parsed_data:
    sessions = get_trial_sessions(date, calendar_id=entry['id'])
    print(sessions)









