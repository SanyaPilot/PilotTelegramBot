from aiogram.types import Message
from init import bot, dp, tw, Notes, session
import logging


@dp.message_handler(commands='notes')
async def notes(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        text = '━━━━━━━━━━━━━━━━━━━━\n' + trans['note']['notes']['list'] + '\n━━━━━━━━━━━━━━━━━━━━\n'
        for name in session.query(Notes.name).all():
            text += '\u2022 '
            text += "<code>" + name[0] + "</code>"
            text += '\n'

        text += '\n'
        text += trans['note']['notes']['instruction']
        await message.reply(text=text, parse_mode='HTML')

    except Exception as e:
        await message.reply(trans['global']['errors']['default'])
        logging.error(e)


@dp.message_handler(commands='note')
async def note(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        msg_id = session.query(Notes.message_id).filter_by(name=message.text.split()[1], chat_id=message.chat.id).first()

        await bot.forward_message(message.chat.id, message.chat.id, msg_id[0])

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
            name = message.text.split()[1]
            if not session.query(Notes.name).filter_by(name=name, chat_id=message.chat.id).first() == (name,):
                session.add(Notes(name=name, message_id=message.reply_to_message.message_id, chat_id=message.chat.id))
                session.commit()
                await message.reply(trans['note']['addnote'])
            else:
                await message.reply(trans['note']['dublicate_err'])
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
            session.query(Notes).filter_by(name=message.text.split()[1], chat_id=message.chat.id).delete()
            session.commit()
            await message.reply(trans['note']['delnote'])
        else:
            await message.reply(trans['global']['errors']['admin'])

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(lambda c: c.text[0] == '#')
async def text_handler(message: Message):
    msg_id = session.query(Notes.message_id).filter_by(name=message.text[1:], chat_id=message.chat.id).first()
    await bot.forward_message(message.chat.id, message.chat.id, msg_id[0])
