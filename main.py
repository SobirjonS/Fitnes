import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from celery_config import app

  
def get_trial_sessions(date, calendar_id):
    url = f'https://acuityscheduling.com/api/v1/appointments'
    
    headers = {
        "accept": "application/json",
        "authorization": "Basic MTc2Njk0OTk6YWFiYTdhMjlkMzNhOGJhN2NiMjc1MGY2YmNkZjFkNGU="
    }
    
    params = {
        'minDate': date,
        'maxDate': date,
        'calendarID': calendar_id
    }
    response = requests.get(url, headers=headers, params=params)
    return  response.content

def text_to_excel(data):
    df = pd.DataFrame(data)

    summary = df.groupby('calendar').agg(
        total_sessions=('calendar', 'count'),
        completed_sessions=('canceled', lambda x: (x == False).sum()),
        canceled_sessions=('canceled', lambda x: x.sum())
    ).reset_index()

    summary = summary.rename(columns={
        'calendar': 'Coach Name',
        'total_sessions': 'Trials Scheduled Till Today',
        'completed_sessions': 'Completed Trials Till Today',
        'canceled_sessions': 'Trials Cancelled/No Show'
    })

    print(summary)

    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')

    calendar_name = df['calendar'].iloc[0].replace(" ", "_")

    file_name = f"files/{calendar_name}_{yesterday_str}.xlsx"

    summary.to_excel(file_name, index=False)

    print(f"Файл успешно создан: {file_name}")
    
    
@app.task
def get_data():
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
        data = get_trial_sessions(date, calendar_id=entry['id'])
        decoded_data = data.decode('utf-8')
        parsed_data = json.loads(decoded_data)
        if parsed_data:
            text_to_excel(data=parsed_data)