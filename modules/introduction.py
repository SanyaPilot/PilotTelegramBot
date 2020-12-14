from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ChatType
from init import bot, dp, engine, Chats
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert
import sqlite3
import logging


@dp.message_handler(commands='start')
async def start(message: Message):
    connection = engine.connect()
    try:  
        if message.chat.type == ChatType.SUPER_GROUP or message.chat.type == ChatType.GROUP:
            connection.execute(insert(Chats).values(chat_id=message.chat.id, setup_is_finished=False, greeting='', leave_msg=''))
            logging.info("Чат " + message.chat.title + " был добавлен в БД")
    except Exception:
        pass
    await bot.send_message(message.chat.id, 'Хай, я бот для чата')
    

    


@dp.message_handler(commands='help')
async def help(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return

    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    curs.execute("""SELECT language FROM chats
                    WHERE chat_id = ?
                          AND setup_is_finished = ?""", (message.chat.id, 1))
    rows = curs.fetchall()
    conn.close()
    if not rows:
        text = trans['global']['errors']['setup']
    else:
        text = trans['introduction']['help']

    await bot.send_message(chat_id=message.chat.id,
                           text=text)


@dp.callback_query_handler(lambda c: 'lang' in c.data)
async def call_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    try:
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                           user_id=call.message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            curs.execute("""UPDATE chats
                            SET language = ?,
                                setup_is_finished = ?
                            WHERE chat_id = ?""", (call.data[5:], 1, call.message.chat.id))
            conn.commit()
            conn.close()
            trans = tw.get_translation(call)
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['lang_set'])

            keyboard = InlineKeyboardMarkup(row_width=2)
            for i in tw.available:
                name = i.split('.')[0]
                keyboard.add(
                    InlineKeyboardButton(text=tw.get_labels()[name], callback_data=f'lang_{name}'))
            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=trans['introduction']['start'],
                                        reply_markup=keyboard)

        else:
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['global']['errors']['admin'])
    except Exception:
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=trans['global']['errors']['default'])
