import asyncio

from aiogram import executor

from init import dp
from modules import introduction

if __name__ == '__main__':
    executor.start_polling(dp)
