from aiogram import executor, Dispatcher
from init import dp, sched
from loguru import logger
from modules import introduction, mute, ban, kick, perms, greeting, note, messages, translate, weather, admin, warn
from modules.settings import settings

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
