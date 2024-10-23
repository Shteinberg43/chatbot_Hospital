import asyncio
import os

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.start import start_router
from handlers.admin import admin_r
from handlers.doctor import doctor_r

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_routers(start_router,admin_r,doctor_r)
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())