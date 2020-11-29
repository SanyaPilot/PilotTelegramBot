import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.types import User
import config
from translation import TranslationWorker

bot = Bot(config.token)
dp = Dispatcher(bot)

tw = TranslationWorker()

conn = sqlite3.connect('data.db')
curs = conn.cursor()

table = """ CREATE TABLE IF NOT EXISTS notes (
                id integer PRIMARY KEY,
                name text NOT NULL,
                message_id integer NOT NULL,
                chat_id integer NOT NULL
            ); """
curs.execute(table)

table = """ CREATE TABLE IF NOT EXISTS chats (
                id integer PRIMARY KEY,
                chat_id integer NOT NULL,
                setup_is_finished integer NOT NULL,
                greeting text,
                leave_msg text,
                language text
            ); """
curs.execute(table)
conn.commit()
conn.close()
