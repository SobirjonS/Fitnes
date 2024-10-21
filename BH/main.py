import requests
import json
import pandas as pd
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
first_day_of_month = datetime.now().replace(day=1).strftime('%Y-%m-%d')

def get_trial_sessions(first_day_of_month, yesterday, calendar_id):
    url = 'https://acuityscheduling.com/api/v1/appointments?showall=true'
    
    headers = {
        "accept": "application/json",
        "authorization": "Basic MTY4Mjg1OTE6Yjk2MzE0YTA4NTQ0NDIzYjdkMjFjYWQ1NzYzZTg4MGI="
    }
    
    params = {
        'minDate': first_day_of_month,
        'maxDate': yesterday,
        'calendarID': calendar_id
    }
    
    response = requests.get(url, headers=headers, params=params)
    appointments = json.loads(response.content.decode('utf-8'))
    
    trial_sessions = [session for session in appointments if 'trial session' in session.get('category').lower()]
    
    return trial_sessions

def collect_all_sessions():
    global first_day_of_month, yesterday

    url = "https://acuityscheduling.com/api/v1/calendars"

    headers = {
        "accept": "application/json",
        "authorization": "Basic MTY4Mjg1OTE6Yjk2MzE0YTA4NTQ0NDIzYjdkMjFjYWQ1NzYzZTg4MGI="
    }
 
    response = requests.get(url, headers=headers)
    calendars = json.loads(response.content.decode('utf-8'))  

    all_data = []

    for entry in calendars:
        sessions = get_trial_sessions(first_day_of_month, yesterday, calendar_id=entry['id'])
        if not sessions:
            all_data.append({
                'calendar': entry['name'],
            })
        else:
            for session in sessions:
                all_data.append(session)
    
    return all_data

def save_to_excel(data):
    global yesterday

    # Создание списка для сбора данных по каждому тренеру
    processed_data = []

    # Проходим по каждому элементу в данных
    for item in data:
        if 'id' in item:  # Если есть id, значит это сессия
            canceled = item.get('canceled', False)
            processed_data.append({
                'Coach Name': item['calendar'],  # Имя тренера
                'Trials Scheduled Till Today': 1,  # Сессия засчитывается
                'Completed Trials Till Today': 0 if canceled else 1,  # Если не отменена, то завершена
                'Trials Cancelled/No Show': 1 if canceled else 0  # Если отменена
            })
        else:  # Если только имя тренера без сессий
            processed_data.append({
                'Coach Name': item['calendar'],
                'Trials Scheduled Till Today': 0,
                'Completed Trials Till Today': 0,
                'Trials Cancelled/No Show': 0
            })

    # Преобразуем в DataFrame
    df = pd.DataFrame(processed_data)

    # Группируем данные по тренерам и суммируем значения
    summary = df.groupby('Coach Name').agg(
        Trials_Scheduled_Till_Today=('Trials Scheduled Till Today', 'sum'),
        Completed_Trials_Till_Today=('Completed Trials Till Today', 'sum'),
        Trials_Cancelled_No_Show=('Trials Cancelled/No Show', 'sum')
    ).reset_index()

    # Переименовываем столбцы
    summary = summary.rename(columns={
        'Coach Name': 'Coach Name',
        'Trials_Scheduled_Till_Today': 'Trials Scheduled Till Today',
        'Completed_Trials_Till_Today': 'Completed Trials Till Today',
        'Trials_Cancelled_No_Show': 'Trials Cancelled/No Show'
    })

    # Сохранение в Excel
    file_name = f"BH/files/BH Trials Report {yesterday}.xlsx"
    summary.to_excel(file_name, index=False)

# # Основной процесс
all_sessions = collect_all_sessions()
if all_sessions:
    save_to_excel(all_sessions)