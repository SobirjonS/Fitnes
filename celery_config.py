from celery import Celery
from celery.schedules import crontab

# Создаем экземпляр приложения Celery и подключаемся к Redis в Docker
app = Celery('tasks', broker='redis://localhost:6379/0')

# Настройки периодических задач
app.conf.beat_schedule = {
    'task_one': {
        'task': 'main.get_data',  # Первая задача
        'schedule': crontab(hour=11, minute=50),  # Выполнять каждый день в 10:00
    },
    'task_two': {
        'task': 'telegrambot.send_data',  # Вторая задача
        'schedule': crontab(hour=11, minute=52),  # Выполнять каждый день в 12:00
    },
}
app.conf.timezone = 'UTC'