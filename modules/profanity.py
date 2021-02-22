from loguru import logger
logger.info('Starting ProfanityFilter import. This may take a while...')
from profanity_filter import ProfanityFilter
from init import bot, dp
from aiogram.types import Message
ru = ProfanityFilter(languages=['ru', 'en'])
en = ProfanityFilter(languages=['en'])
logger.info('ProfanityFilter init           [ OK ]')

whitelist = ['клонируй', 'разраб']


@dp.message_handler()
async def greeting(message: Message):
    for word in message.text.split():
        print(word in whitelist)
        print(ru.censor_word(word).original_profane_word)
        if word.lower() not in whitelist and (ru.censor_word(word).original_profane_word or en.censor_word(word).original_profane_word):
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(message.chat.id, "Мат, ууу")
            logger.info(f"{message.chat.full_name}: {message.from_user.full_name} - profanity!")

