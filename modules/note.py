from aiogram.types import Message
from init import bot, dp, tw, Notes, session
from loguru import logger


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
        logger.info(f"{message.chat.full_name}: {message.from_user.full_name} - notes")
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(commands='note')
async def note(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if len(message.text.split()) == 2:
            msg_id = session.query(Notes.message_id).filter_by(name=message.text.split()[1], chat_id=message.chat.id).first()

            await bot.forward_message(message.chat.id, message.chat.id, msg_id[0])
            logger.info(f"{message.chat.full_name}: {message.from_user.full_name} - note")
        else:
            await message.reply(trans['global']['errors']['no_args'])
            logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without args')
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(commands='addnote')
async def addnote(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            if len(message.text.split()) == 2:
                member = await bot.get_chat_member(chat_id=message.chat.id,
                                                   user_id=message.from_user.id)
                if member.status == 'creator' or member.status == 'administrator':
                    name = message.text.split()[1]
                    if not session.query(Notes.name).filter_by(name=name, chat_id=message.chat.id).first() == (name,):
                        session.add(Notes(name=name, message_id=message.reply_to_message.message_id, chat_id=message.chat.id))
                        session.commit()
                        await message.reply(trans['note']['addnote'])
                        logger.info(f"{message.chat.full_name}: New note - {name}")
                    else:
                        await message.reply(trans['note']['dublicate_err'])
                        logger.warning(f"{message.chat.full_name}: {message.from_user.full_name} - Such note already exists")
                else:
                    await message.reply(trans['global']['errors']['admin'])
                    logger.warning(
                        f"{message.chat.full_name}: User {message.from_user.full_name} need administrative privileges to do this")
            else:
                await message.reply(trans['global']['errors']['no_args'])
                logger.warning(
                    f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without args')
        else:
            await message.reply(trans['global']['errors']['no_reply'])
            logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without reply')
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(commands='rmnote')
async def rmnote(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if len(message.text.split()) == 2:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                if session.query(Notes.name).filter_by(name=message.text.split()[1], chat_id=message.chat.id).first():
                    session.query(Notes).filter_by(name=message.text.split()[1], chat_id=message.chat.id).delete()
                    session.commit()
                    await message.reply(trans['note']['delnote'])
                    logger.info(f"{message.chat.full_name}: rm note - {message.text.split()[1]}")
                else:
                    await message.reply(trans['note']['no_such_note_err'])
                    logger.warning(f"{message.chat.full_name}: Note {message.text.split()[1]} does not exist")
            else:
                await message.reply(trans['global']['errors']['admin'])
                logger.warning(
                    f"{message.chat.full_name}: User {message.from_user.full_name} need administrative privileges to do this")
        else:
            await message.reply(trans['global']['errors']['no_args'])
            logger.warning(
                f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without args')
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(lambda c: c.text[0] == '#')
async def text_handler(message: Message):
    try:
        msg_id = session.query(Notes.message_id).filter_by(name=message.text[1:], chat_id=message.chat.id).first()
        await bot.forward_message(message.chat.id, message.chat.id, msg_id[0])
        logger.info(f"{message.chat.full_name}: {message.from_user.full_name} - #{message.text[1:]}")
    except Exception:
        logger.warning(f"{message.chat.full_name}: this chat dont have {message.text[1:]}")
