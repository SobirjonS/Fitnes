import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

TELEGRAM_TOKEN = '7338375924:AAFHdwHEdtVXK70HJw2lfbMPi8lm7OrMHG0'
CHAT_ID = '-1002217060475'

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode=ParseMode.HTML)
        print("Сообщение отправлено!")
    except TelegramError as e:
        print(f"Ошибка при отправке сообщения: {e}")

message = "Количество проведенных сессий за вчера: 5"

async def main():
    await send_telegram_message(message)

if __name__ == "__main__":
    asyncio.run(main())
