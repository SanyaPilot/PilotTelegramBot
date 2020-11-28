from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from init import bot, dp, tw
from threading import Timer
import sqlite3

timers = {}


@dp.message_handler(content_types='new_chat_members')
async def greeting(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        curs.execute('SELECT * FROM chats WHERE chat_id = ?', (message.chat.id,))
        result = curs.fetchall()
        conn.close()
        try:
            row = result[0]
            new_user = message.new_chat_members[0]
            if row[2] == 1 and row[3] and not new_user.is_bot:
                keyboard = InlineKeyboardMarkup()
                key = InlineKeyboardButton(text=trans['greeting']['greeting'], callback_data='captcha_ok')
                keyboard.add(key)

                await bot.send_message(chat_id=message.chat.id,
                                       reply_to_message_id=message.message_id,
                                       parse_mode='HTML',
                                       text=row[3],
                                       reply_markup=keyboard)

                await bot.restrict_chat_member(chat_id=message.chat.id,
                                               user_id=new_user.id,
                                               can_send_messages=False,
                                               until_date=0)

                global timers
                timers[message.from_user.id] = Timer(300.0, kick_bot, [message.chat.id, message.from_user.id, message])
                timers[message.from_user.id].start()
        except IndexError:
            pass
    except Exception:
        await message.reply(trans['global']['errors']['default'])


async def kick_bot(chat_id, user_id, message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        await bot.kick_chat_member(chat_id=chat_id,
                                   user_id=user_id,
                                   until_date=0)

        await bot.unban_chat_member(chat_id=chat_id,
                                    user_id=user_id)

        chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        user = chat_member.user
        await bot.send_message(chat_id=chat_id,
                               text=trans['greeting']['kick_bot'].format(username=str(user.username)))
        global timers
        timers.pop(user_id)

    except Exception:
        pass


@dp.message_handler(commands='setgreeting')
async def set_greeting(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            try:
                conn = sqlite3.connect('data.db')
                curs = conn.cursor()
                curs.execute('SELECT setup_is_finished FROM chats WHERE chat_id = ?', (message.chat.id,))
                result = curs.fetchall()
                if result[0][0] == 1:
                    curs.execute("""UPDATE chats
                                    SET greeting = ?
                                    WHERE chat_id = ?""", (message.reply_to_message.text, message.chat.id))
                    conn.commit()
                    await message.reply(trans['greeting']['set_greeting'])

                conn.close()
            except Exception:
                await message.reply(trans['global']['errors']['setup'])
        else:
            await message.reply(trans['global']['errors']['admin'])
    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='rmgreeting')
async def rm_greeting(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            try:
                conn = sqlite3.connect('data.db')
                curs = conn.cursor()
                curs.execute('SELECT setup_is_finished FROM chats WHERE chat_id = ?', (message.chat.id,))
                result = curs.fetchall()
                if result[0][0] == 1:
                    curs.execute("""UPDATE chats
                                    SET greeting = ?
                                    WHERE chat_id = ?""", ('', message.chat.id))
                    conn.commit()
                    await message.reply(trans['greeting']['rm_greeting'])

                conn.close()
            except Exception:
                await message.reply(trans['global']['errors']['setup'])
        else:
            await message.reply(trans['global']['errors']['admin'])
    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='setleavemsg')
async def set_user_leave_msg(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            try:
                conn = sqlite3.connect('data.db')
                curs = conn.cursor()
                curs.execute('SELECT setup_is_finished FROM chats WHERE chat_id = ?', (message.chat.id,))
                result = curs.fetchall()
                if result[0][0] == 1:
                    curs.execute("""UPDATE chats
                                    SET leave_msg = ?
                                    WHERE chat_id = ?""", (message.reply_to_message.text, message.chat.id))
                    conn.commit()
                    await message.reply(trans['greeting']['set_user_leave_msg'])

                conn.close()
            except Exception:
                await message.reply(trans['global']['errors']['setup'])
        else:
            await message.reply(trans['global']['errors']['admin'])
    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='rmleavemsg')
async def rm_user_leave_msg(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            try:
                conn = sqlite3.connect('data.db')
                curs = conn.cursor()
                curs.execute('SELECT setup_is_finished FROM chats WHERE chat_id = ?', (message.chat.id,))
                result = curs.fetchall()
                if result[0][0] == 1:
                    curs.execute("""UPDATE chats
                                    SET leave_msg = ?
                                    WHERE chat_id = ?""", ('', message.chat.id))
                    conn.commit()
                    await message.reply(trans['greeting']['rm_user_leave_msg'])

                conn.close()
            except Exception:
                await message.reply(trans['global']['errors']['setup'])
        else:
            await message.reply(trans['global']['errors']['admin'])
    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(content_types='left_chat_member')
async def user_leave_msg(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        conn = sqlite3.connect('data.db')
        curs = conn.cursor()
        curs.execute('SELECT * FROM chats WHERE chat_id = ?', (message.chat.id,))
        result = curs.fetchall()
        conn.close()
        try:
            row = result[0]
            if row[2] == 1 and row[4]:
                await bot.send_message(chat_id=message.chat.id,
                                       reply_to_message_id=message.message_id,
                                       parse_mode='HTML',
                                       text=row[4])
        except IndexError:
            pass
    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.callback_query_handler(lambda c: c.data == 'captcha_ok')
async def call_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    if trans == 1:
        return
    try:
        timers[call.from_user.id].cancel()

        chat = await bot.get_chat(chat_id=call.message.chat.id)
        perms = chat.permissions
        await bot.restrict_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id,
                                       can_send_messages=True,
                                       can_send_media_messages=perms.can_send_media_messages,
                                       can_send_other_messages=perms.can_send_other_messages,
                                       can_add_web_page_previews=perms.can_add_web_page_previews,
                                       until_date=0)

        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=trans['greeting']['check_success'])
        timers.pop(call.from_user.id)
    except KeyError:
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=trans['greeting']['other_user_err'])
