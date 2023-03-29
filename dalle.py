#!/usr/bin/python3

import os
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


tg_token = os.getenv("TG_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
users_ids = (os.getenv("USER1_TG_ID"),)

bot = Bot(tg_token)
dp = Dispatcher(bot)
users_access = lambda message : message.from_user.id in users_ids



@dp.message_handler(users_access, content_types=['any'])
# @dp.message_handler()
async def send(message : types.Message):
    response = openai.Image.create(
        prompt=message.text,
        n=1,
        size="1024x1024"
    )
    # await message.answer(message.from_user.id)
    try:
        await message.answer(response['data'][0]['url'])
    except Exception as ex:
        await message.answer("something was wrong")
        # TODO: log this


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
