"""
Open AI gpt-3.5-turbo model Python Bot implementation.
"""

#!/usr/bin/python3

import os
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from cachetools import LRUCache
from ext.filters import MentionedMe, RepliedMe
from ext.logger import Logger


DEFAULT_AI_CONTENT = "You are a helpful assistant."
WELCOME_MESSAGE = "Hi! I am Chat GPT and I am ready to help You"
MODEL_ENGINE = "gpt-3.5-turbo"
HELP_INFO = """
Chat GPT implementation using 3.5 model.
To start a conversation with a new context just tag the bot, e.g.
@gpt3father_bot What is the diameter of the Earth?.
"""

tg_token = os.getenv("TG_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
users_ids = (os.getenv("USER1_TG_ID"),)

bot = Bot(tg_token)
dp = Dispatcher(bot)
messages_history = LRUCache(maxsize=128 * 1024 * 1024) # 128mb cache
logger = Logger('log/bot_log.log')


@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await message.answer(HELP_INFO)

@dp.message_handler(commands=['reset'], user_id=users_ids)
async def command_handler(message : types.Message):
    global messages_history
    messages_history = LRUCache(maxsize=128 * 1024 * 1024)
    messages_history[message.from_user.id] = [{"role": "system", "content": DEFAULT_AI_CONTENT},]
    await message.answer(WELCOME_MESSAGE)

@dp.message_handler(MentionedMe(), content_types=['any'])
async def reply_to_mention(message: types.Message):
    global messages_history
    user_id = message.from_user.id
    try:
        messages_history[user_id] = [{"role": "system", "content": DEFAULT_AI_CONTENT},]
        messages_history[user_id].append({"role": "user", "content": message.text},)
        response = openai.ChatCompletion.create(
            model=MODEL_ENGINE,
            messages=messages_history[user_id],
            temperature=0.2,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=""
        )
        ai_response = response['choices'][0]['message']['content']
        messages_history[user_id].append({"role": "system", "content": ai_response},)
        await bot.send_message(
            chat_id=message.chat.id,
            text=ai_response,
            reply_to_message_id=message.message_id
        )
    except KeyError:
        logger.error(f'user id={user_id} not found in messages_history')


@dp.message_handler(RepliedMe(), content_types=['any'])
async def reply_to_reply(message: types.Message):
    global messages_history
    user_id = message.from_user.id
    try:
        if user_id not in messages_history.keys():
            messages_history[user_id]=[{"role": "system", "content": DEFAULT_AI_CONTENT},]
            messages_history[user_id].append(
                {
                    "role": "system",
                    "content": message.reply_to_message.text
                },
            )
        messages_history[user_id].append({"role": "user", "content": message.text},)
        response = openai.ChatCompletion.create(
            model=MODEL_ENGINE,
            messages=messages_history[user_id],
            temperature=0.2,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=""
        )
        ai_response = response['choices'][0]['message']['content']
        messages_history[user_id].append({"role": "system", "content": ai_response},)
        await bot.send_message(
            chat_id=message.chat.id,
            text=ai_response,
            reply_to_message_id=message.message_id
        )
    except KeyError:
        logger.error(f'user id={user_id} not found in messages_history')


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
