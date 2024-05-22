import asyncio
from aiogram import types, Bot, Dispatcher
from aiogram.filters import CommandStart, Command


from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Hi {message.from_user.full_name}")




@dp.message()
async def echo(message: types.Message):
    print(message.text)
    await bot.send_message(message.from_user.id, message.text)





async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)




asyncio.run(main())

