from aiogram import executor, Dispatcher
from init import dp, sched
from loguru import logger

from modules import antispam
from modules import introduction, greeting
from modules.settings import settings
from modules import perms, admin, warn
from modules import mute, ban, kick
from modules import note, messages, translate, weather
from modules import triggers

logger.info('Init finished! Starting polling...')


async def on_startup(dp: Dispatcher):
    sched.start()
    logger.info('APScheduler start        [ OK ]')
    logger.info('Polling start            [ OK ]')


async def on_shutdown(dp: Dispatcher):
    logger.info('Stopping APScheduler. If it has current jobs this may take a while...')
    sched.shutdown()
    logger.info('APScheduler stop            [ OK ]')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

