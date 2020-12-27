from aiogram import executor
from init import dp
from modules import introduction, mute, ban, kick, perms, greeting, note, messages, translate, weather

if __name__ == '__main__':
    executor.start_polling(dp)
