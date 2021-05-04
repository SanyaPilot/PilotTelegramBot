import sys
import os
import shutil
from loguru import logger

# AIOGram imports
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

# SQLAlchemy imports
from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String,
                        text, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Misc imports
from utils.translation import TranslationWorker

from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger.info('Welcome to PilotTelegramBot!')
logger.info('Starting init...')

docker_init = False
if os.path.exists('config.py'):
    logger.info('Normal init')
    import config
elif os.path.exists('/config/') and not os.path.exists('/config/config.py'):
    logger.info('Docker first start init')
    shutil.copyfile('config.example', '/config/config.py')
    logger.info('Now fill lines in config.py and restart container again')
    sys.exit(0)
elif os.path.exists('/config/config.py'):
    logger.info('Docker init')
    docker_init = True
    sys.path.insert(1, '/config')
    import config
else:
    logger.error("Can't init! If starting in normal way, check config.py. If starting as Docker container, "
                 "apply RW bind-mount to /config container's directory")
    sys.exit(1)

bot = Bot(config.token)

# FSM enabling
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logger.info('AIOgram init                   [ OK ]')
logger.info('Jumping to Telethon init...')


# FSM states
class FirstStartWarnStates(StatesGroup):
    set_max = State()
    set_punishment = State()
    set_time = State()


class WarnStates(StatesGroup):
    set_max = State()
    set_punishment = State()
    set_time = State()


class GreetingStates(StatesGroup):
    set_greeting = State()
    set_leave_msg = State()


class SettingsStates(StatesGroup):
    menu = State()
    warns = State()
    greeting = State()

# Initialising telethon
import modules.telethon.init

# SQL stuff
Base = declarative_base()


class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    message_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    chat = relationship("Chats", backref='Chat')


class Warns(Base):
    __tablename__ = 'warns'
    user_id = Column(Integer, primary_key=True)
    warns = Column(Integer, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))


class Chats(Base):
    __tablename__ = "chats"
    chat_id = Column(Integer, primary_key=True)
    helper_in_chat = Column(Boolean, nullable=False)
    max_warns = Column(Integer, nullable=False)
    warns_punishment = Column(String)
    warns_punishment_time = Column(Integer)
    greeting = Column(String)
    leave_msg = Column(String)
    language = Column(String, server_default=text('rus'))


if docker_init:
    engine = create_engine("sqlite:////config/db.sqlite", )
else:
    engine = create_engine("sqlite:///db.sqlite", )

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
logger.info('SQL Alchemy init               [ OK ]')

tw = TranslationWorker(session, Chats, config.default_lang)
logger.info('TranslationWorker init         [ OK ]')

sched = AsyncIOScheduler()
logger.info('APScheduler init               [ OK ]')
