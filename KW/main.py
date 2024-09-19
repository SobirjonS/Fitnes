import requests
import json
import pandas as pd
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

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
    return json.loads(response.content.decode('utf-8'))

def collect_all_sessions():
    global yesterday
    url = "https://acuityscheduling.com/api/v1/calendars"
    headers = {
        "accept": "application/json",
        "authorization": "Basic MTc2Njk0OTk6YWFiYTdhMjlkMzNhOGJhN2NiMjc1MGY2YmNkZjFkNGU="
    }

    response = requests.get(url, headers=headers)
    calendars = json.loads(response.content.decode('utf-8'))

    all_data = []  # Здесь будут собраны данные всех тренеров

    for entry in calendars:
        sessions = get_trial_sessions(yesterday, calendar_id=entry['id'])
        if not sessions:  # Если сессий нет, добавляем нулевые значения
            all_data.append({
                'calendar': entry['name'],
                'canceled': None  # Добавляем столбец canceled как None или False
            })
        else:
            for session in sessions:
                all_data.append(session)

    return all_data

def save_to_excel(data):
    global yesterday

    df = pd.DataFrame(data)

    # Заполняем NaN значениями для столбца 'canceled', если нет данных
    df['canceled'] = df['canceled'].fillna(True)  # Можно задать False, если это необходимо

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

    file_name = f"KW/files/KW Trials Report {yesterday}.xlsx"
    summary.to_excel(file_name, index=False)

# Основной процесс
all_sessions = collect_all_sessions()
if all_sessions:
    save_to_excel(all_sessions)