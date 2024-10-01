import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Получаем вчерашнюю дату
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

# Переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID_BH")

# Путь к конкретному файлу
FILE_PATH = f"BH/files/BH Trials Report {yesterday}.xlsx"

# Функция для отправки файла
async def send_file(file_path):
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        with open(file_path, 'rb') as file:
            await bot.send_document(chat_id=CHAT_ID, document=file)
        print(f"Файл {file_path} отправлен!")
    except TelegramError as e:
        print(f"Ошибка при отправке файла {file_path}: {e}")

# Главная функция
async def main():
    # Проверяем, существует ли файл
    if os.path.isfile(FILE_PATH):
        await send_file(FILE_PATH)
    else:
        print(f"Файл {FILE_PATH} не найден!")

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
