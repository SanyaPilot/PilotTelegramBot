from aiogram.types import Message, ContentType
from init import bot, dp, tw, Triggers, session
from loguru import logger


@dp.message_handler(commands='triggers')
async def triggers(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        text = '━━━━━━━━━━━━━━━━━━━━\n' + trans['trigger']['list'] + '\n━━━━━━━━━━━━━━━━━━━━\n'
        for name in session.query(Triggers.word).filter_by(chat_id=message.chat.id).all():
            text += '\u2022 '
            text += "<code>" + name[0] + "</code>"
            text += '\n'

        await message.reply(text=text, parse_mode='HTML')
        logger.info(f"{message.chat.full_name}: {message.from_user.full_name} - triggers")
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")


@dp.message_handler(commands='addtrigger')
async def addtrigger(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            if len(message.text.split()) == 2:
                member = await bot.get_chat_member(chat_id=message.chat.id,
                                                   user_id=message.from_user.id)
                if member.status == 'creator' or member.status == 'administrator':
                    word = message.text.split()[1].lower()
                    if not session.query(Triggers.word).filter_by(word=word, chat_id=message.chat.id).first() == (word,):
                        session.add(Triggers(word=word, message_id=message.reply_to_message.message_id, chat_id=message.chat.id))
                        session.commit()
                        await message.reply(trans['trigger']['addtrigger'])
                        logger.info(f"{message.chat.full_name}: New trigger - {word}")
                    else:
                        await message.reply(trans['trigger']['dublicate_err'])
                        logger.warning(f"{message.chat.full_name}: {message.from_user.full_name} - Such trigger already exists")
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


@dp.message_handler(commands='rmtrigger')
async def rmtrigger(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if len(message.text.split()) == 2:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                word = message.text.split()[1].lower()
                if session.query(Triggers.word).filter_by(word=word, chat_id=message.chat.id).first():
                    session.query(Triggers).filter_by(word=word, chat_id=message.chat.id).delete()
                    session.commit()
                    await message.reply(trans['trigger']['deltrigger'])
                    logger.info(f"{message.chat.full_name}: rm trigger - {message.text.split()[1]}")
                else:
                    await message.reply(trans['trigger']['no_such_trigger_err'])
                    logger.warning(f"{message.chat.full_name}: Trigger {message.text.split()[1]} does not exist")
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


@dp.message_handler(content_types=ContentType.TEXT)
async def process_trigger(message: Message):
    triggers = session.query(Triggers.word, Triggers.message_id).filter_by(chat_id=message.chat.id).all()
    for trigger in triggers:
        delimiters = [",", ".", "!", "?", "/", "&", "-", ":", ";", "@", "'", "..."]
        text = message.text.lower()
        for delimiter in delimiters:
            text = text.replace(delimiter, ' ')

        if trigger[0] in text.split():
            try:
                await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=trigger[1],
                                       parse_mode='HTML', reply_to_message_id=message.message_id)
            except Exception:
                session.query(Triggers).filter_by(word=trigger[0], chat_id=message.chat.id).delete()
                session.commit()
                logger.warning(f"{message.chat.full_name}: Reply msg for trigger {trigger[0]} is not found")
                return
