from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class MentionedMe(BoundFilter):
    key = 'mentioned_me'

    def __init__(self, replied_only=False):
        self.replied_only = replied_only

    async def check(self, message: Message) -> bool:
        bot_info = await message.bot.get_me()
        if self.replied_only:
            # Проверяем, что сообщение является ответом на сообщение бота
            return message.reply_to_message and message.reply_to_message.from_user.id == message.bot.id and message.text and f"@{bot_info.username}" in message.text
        else:
            # Проверяем, что бот был упомянут в тексте сообщения
            return message.text and f"@{bot_info.username}" in message.text


class RepliedMe(BoundFilter):
    key = 'replied_me'

    def __init__(self, include_edited=False):
        self.include_edited = include_edited

    async def check(self, message: Message) -> bool:
        if message.reply_to_message:
            replied_message = message.reply_to_message
            if replied_message.from_user and replied_message.from_user.is_bot:
                bot_info = await message.bot.get_me()
                if replied_message.from_user.id == bot_info.id:
                    if self.include_edited:
                        return True
                    else:
                        return not replied_message.edit_date
        return False
