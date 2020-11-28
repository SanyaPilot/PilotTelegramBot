from aiogram.types import Message
from init import bot, dp, tw
import sqlite3


@dp.message_handler(commands='notes')
async def notes(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        cmd = """ SELECT name FROM notes
                  WHERE chat_id = ?"""

        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        curs.execute(cmd, (message.chat.id,))
        rows = curs.fetchall()
        conn.close()
        text = '━━━━━━━━━━━━━━━━━━━━\n' + trans['note']['notes']['list'] + '\n━━━━━━━━━━━━━━━━━━━━\n'
        for row in rows:
            text += '\u2022 '
            text += "<code>" + row[0] + "</code>"
            text += '\n'

        text += '\n'
        text += trans['note']['notes']['instruction']
        await message.reply(text=text, parse_mode='HTML')

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='note')
async def note(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        words = message.text.split()
        name = words[1]
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        cmd = """ SELECT message_id FROM notes
                  WHERE name = ?
                  AND chat_id = ?"""
        curs.execute(cmd, (name, message.chat.id))

        rows = curs.fetchall()

        conn.close()

        row = rows[0]
        await bot.forward_message(message.chat.id, message.chat.id, row[0])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='addnote')
async def addnote(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            words = message.text.split()
            name = words[1]
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            cmd = """ INSERT INTO notes(name, message_id, chat_id)
                      VALUES(?,?,?) """
            params = (name, message.reply_to_message.message_id, message.chat.id)
            curs.execute(cmd, params)
            conn.commit()
            conn.close()

            await message.reply(trans['note']['addnote'])
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='rmnote')
async def rmnote(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            words = message.text.split()
            name = words[1]
            conn = sqlite3.connect('data.db')
            curs = conn.cursor()
            cmd = """ DELETE FROM notes
                      WHERE name = ?
                      AND chat_id = ?"""
            curs.execute(cmd, (name, message.chat.id))
            conn.commit()
            conn.close()

            await message.reply(trans['note']['delnote'])
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(lambda c: c.text[0] == '#')
async def text_handler(message: Message):
    name = message.text[1:]
    conn = sqlite3.connect('data.db')
    curs = conn.cursor()
    cmd = """ SELECT message_id FROM notes
                          WHERE name = ?
                          AND chat_id = ?"""
    curs.execute(cmd, (name, message.chat.id))
    rows = curs.fetchall()
    conn.close()

    row = rows[0]
    await bot.forward_message(message.chat.id, message.chat.id, row[0])
