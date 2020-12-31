from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String,
                        text, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import sqlite3
from loguru import logger

Base = declarative_base()


class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    message_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    chat = relationship("Chats", backref='Chat')


class Chats(Base):
    __tablename__ = "chats"
    chat_id = Column(Integer, primary_key=True)
    setup_is_finished = Column(Boolean, nullable=False)
    greeting = Column(String)
    leave_msg = Column(String)
    language = Column(String, server_default=text('rus'))


engine = create_engine(
            "sqlite:///db.sqlite",
        )
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

logger.info('Starting script...')
logger.info('Getting all data from old db...')
conn = sqlite3.connect('data.db')
curs = conn.cursor()
curs.execute('SELECT * FROM chats')
old_chats = curs.fetchall()
curs.execute('SELECT * FROM notes')
old_notes = curs.fetchall()
logger.info('Writing chats data to new db...')
for row in old_chats:
    if row[1] < 0:
        session.add(Chats(chat_id=row[1], setup_is_finished=row[2], greeting=row[3], leave_msg=row[4], language=row[5]))

logger.info('Writing notes data to new db...')
for row in old_notes:
    session.add(Notes(id=row[0], name=row[1], message_id=row[2], chat_id=row[3]))

session.commit()
logger.info('Commited changes')