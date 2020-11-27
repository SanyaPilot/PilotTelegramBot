from aiogram import executor
from init import dp

#from modules import introduction, translate, ban, greeting, kick, messages, mute, note, perms, weather, admin
from modules import introduction, mute, ban


if __name__ == '__main__':
    executor.start_polling(dp)
