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
async def send(message : types.Message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.6,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop="You:"
    )
    await message.answer(response['choices'][0]['text'])


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
