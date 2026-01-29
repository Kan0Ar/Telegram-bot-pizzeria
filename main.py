import os
from dotenv import find_dotenv, load_dotenv
import logging
import asyncio
from aiogram import Bot, Dispatcher, Router, F
from app_hk.handlers import router


load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))

dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

