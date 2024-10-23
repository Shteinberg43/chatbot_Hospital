from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

start_router = Router()
@start_router.message(CommandStart())
async def start(message: Message):
    await message.answer(text="Здравствуйте, для продолжения работы выберите роль:\n"
                              "Для работы админом - /admin\n"
                              "Для работы врачом - /doctor\n")