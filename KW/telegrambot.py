import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
FILES_DIR = f"/Fitnes/KW/files/KW Trials Report {yesterday}.xlsx"

async def send_file(file_path):
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        with open(file_path, 'rb') as file:
            await bot.send_document(chat_id=CHAT_ID, document=file)
        print(f"Файл {file_path} отправлен!")
    except TelegramError as e:
        print(f"Ошибка при отправке файла {file_path}: {e}")

async def send_files_in_directory(directory):
    tasks = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            tasks.append(send_file(file_path))
    
    await asyncio.gather(*tasks)

async def main():
    await send_files_in_directory(FILES_DIR)

if __name__ == "__main__":
    asyncio.run(main())
