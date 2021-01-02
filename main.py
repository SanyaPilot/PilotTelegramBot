from aiogram import executor
from init import dp
from loguru import logger
from modules import introduction, mute, ban, kick, perms, greeting, note, messages, translate, weather, admin, profanity
logger.info('Init finished! Starting polling...')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=logger.info('Polling start               [ OK ]'))
