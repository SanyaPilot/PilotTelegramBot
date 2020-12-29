from aiogram import executor
from init import dp
from loguru import logger
from modules import introduction, mute, ban, kick, perms, greeting, note, messages, translate, weather, admin

if __name__ == '__main__':
    logger.info('Ok')
    executor.start_polling(dp)
