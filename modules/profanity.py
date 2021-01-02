from loguru import logger
logger.info('Starting ProfanityFilter import. This may take a while...')
from profanity_filter import ProfanityFilter
from init import bot, dp
from aiogram.types import Message
ru = ProfanityFilter(languages=['ru', 'en'])
en = ProfanityFilter(languages=['en'])
logger.info('ProfanityFilter init           [ OK ]')


@dp.message_handler(lambda c: ru.is_profane(c.text))
@dp.message_handler(lambda c: en.is_profane(c.text))
async def greeting(message: Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, "Мат, ууу")
    logger.info(f"{message.chat.full_name}: {message.from_user.full_name} - profanity!")
