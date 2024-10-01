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
CHAT_ID_KSA = os.getenv("CHAT_ID_KSA")
CHAT_ID_KSA2 = os.getenv("CHAT_ID_KSA2")

# Путь к конкретному файлу
FILE_PATH = f"KSA/files/KSA Trials Report {yesterday}.xlsx"

# Функция для отправки файла
async def send_file_1(file_path):
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        with open(file_path, 'rb') as file:
            await bot.send_document(chat_id=CHAT_ID_KSA, document=file)
        print(f"Файл {file_path} отправлен!")
    except TelegramError as e:
        print(f"Ошибка при отправке файла {file_path}: {e}")

async def send_file_2(file_path):
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        with open(file_path, 'rb') as file:
            await bot.send_document(chat_id=CHAT_ID_KSA2, document=file)
        print(f"Файл {file_path} отправлен!")
    except TelegramError as e:
        print(f"Ошибка при отправке файла {file_path}: {e}")

# Главная функция
async def main():
    # Проверяем, существует ли файл
    if os.path.isfile(FILE_PATH):
        await send_file_1(FILE_PATH)
        await send_file_2(FILE_PATH)
    else:
        print(f"Файл {FILE_PATH} не найден!")

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
