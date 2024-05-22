import asyncio
from aiogram import types, Bot, Dispatcher
from aiogram.filters import CommandStart, Command

from aggregate import *

from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Hi {message.from_user.full_name}")




@dp.message()
async def echo(message: types.Message):
    print(message.text)
    #await message.answer('Enter a dataset in format {"dt_from": "2022-01-01T00:00:00",  "dt_upto": "2022-01-01T02:00:00", "group_type": "day"}: ')
    data_dict = json.loads(message.text.replace("'", "\""))
    data = aggregating_data(data_dict['dt_from'], data_dict["dt_upto"], data_dict["group_type"])
    if data:
        await bot.send_message(message.from_user.id, str(data))
    else:
        await message.answer('Enter a dataset in format {"dt_from": "2022-01-01T00:00:00",  "dt_upto": "2022-01-01T02:00:00", "group_type": "day"}: ')




async def main():
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)




asyncio.run(main())

