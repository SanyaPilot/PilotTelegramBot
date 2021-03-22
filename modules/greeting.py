from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from init import bot, dp, tw, Chats, session, sched
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

kick_jobs = {}


@dp.message_handler(content_types='new_chat_members')
async def greeting(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        chat = session.query(Chats.setup_is_finished, Chats.greeting).filter_by(chat_id=message.chat.id).first()
        try:
            new_user = message.new_chat_members[0]
            if chat[0] and chat[1] and not new_user.is_bot:
                keyboard = InlineKeyboardMarkup()

                keyboard.add(InlineKeyboardButton(text=trans['greeting']['greeting'][1], callback_data='captcha_no1'))
                keyboard.add(InlineKeyboardButton(text=trans['greeting']['greeting'][0], callback_data='captcha_ok'))
                keyboard.add(InlineKeyboardButton(text=trans['greeting']['greeting'][2], callback_data='captcha_no2'))

                await bot.send_message(chat_id=message.chat.id,
                                       reply_to_message_id=message.message_id,
                                       parse_mode='HTML',
                                       text=chat[1],
                                       reply_markup=keyboard)

                await bot.restrict_chat_member(chat_id=message.chat.id,
                                               user_id=new_user.id,
                                               can_send_messages=False,
                                               until_date=0)
                logger.info(
                    f"{message.chat.full_name}: New user {new_user.full_name}")
                global kick_jobs
                if kick_jobs.get(message.chat.id) is None:
                    kick_jobs[message.chat.id] = {}

                kick_jobs[message.chat.id][message.new_chat_members[0].id] = sched.add_job(kick_bot,
                                                                                           IntervalTrigger(minutes=5),
                                                                                           [message.chat.id,
                                                                                            message.new_chat_members[0].id,
                                                                                            message])

        except IndexError:
            pass
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: {err}")


async def kick_bot(chat_id, user_id, message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        global kick_jobs
        result = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        if result.status == 'left' or result.status == 'kicked':
            kick_jobs[chat_id][user_id].remove()
            kick_jobs[chat_id].pop(user_id)
            return

        await bot.kick_chat_member(chat_id=chat_id,
                                   user_id=user_id,
                                   until_date=0)

        await bot.unban_chat_member(chat_id=chat_id,
                                    user_id=user_id)

        chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        user = chat_member.user
        if user.username:
            username = user.username
        else:
            username = user.full_name

        await bot.send_message(chat_id=chat_id,
                               text=trans['greeting']['kick_bot'].format(username=str(username)))
        kick_jobs[chat_id][user_id].remove()
        kick_jobs[chat_id].pop(user_id)
        logger.info(
            f"{message.chat.full_name}: is bot {user.full_name}")
    except Exception as e:
        logger.error(e)


@dp.message_handler(commands='setgreeting')
async def set_greeting(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        bot_obj = await bot.get_me()
        bot_id = bot_obj.id
        me = await bot.get_chat_member(chat_id=message.chat.id, user_id=bot_id)
        if me.can_restrict_members:
            if message.reply_to_message:
                member = await bot.get_chat_member(chat_id=message.chat.id,
                                                   user_id=message.from_user.id)
                if member.status == 'creator' or member.status == 'administrator':
                    result = session.query(Chats.setup_is_finished).filter_by(chat_id=message.chat.id).first()
                    if result[0]:
                        chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
                        chat.greeting = message.reply_to_message.text
                        session.commit()
                        await message.reply(trans['greeting']['set_greeting'])
                        logger.info(f"{message.chat.full_name}: new greeting")
                    else:
                        await message.reply(trans['global']['errors']['setup'])
                        logger.warning(f"{message.chat.full_name}: setup greeting")
                else:
                    await message.reply(trans['global']['errors']['admin'])
                    logger.warning(f"{message.chat.full_name}: {message.from_user.full_name} not admin")
            else:
                await message.reply(trans['global']['errors']['no_reply'])
                logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without reply')
        else:
            perm = 'can_restrict_members'
            await message.reply(trans['global']['errors']['no_needed_perm'].format(perm=perm),
                                parse_mode='HTML')
            logger.warning(f"{message.chat.full_name}: Bot doesn't have perm {perm}")
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(
            f"{message.chat.full_name}: {err}")


@dp.message_handler(commands='rmgreeting')
async def rm_greeting(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                result = session.query(Chats.setup_is_finished).filter_by(chat_id=message.chat.id).first()
                if result[0]:
                    chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
                    chat.greeting = ''
                    session.commit()
                    await message.reply(trans['greeting']['rm_greeting'])
                    logger.info(f"{message.chat.full_name}: rm greeting")
                else:
                    await message.reply(trans['global']['errors']['setup'])
                    logger.warning(f"{message.chat.full_name}: setup greeting")
            else:
                await message.reply(trans['global']['errors']['admin'])
                logger.warning(f"{message.chat.full_name}: {message.from_user.full_name} not admin")
        else:
            await message.reply(trans['global']['errors']['no_reply'])
            logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without reply')

    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(
            f"{message.chat.full_name}: {err}")


@dp.message_handler(commands='setleavemsg')
async def set_user_leave_msg(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                result = session.query(Chats.setup_is_finished).filter_by(chat_id=message.chat.id).first()
                if result[0]:
                    chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
                    chat.leave_msg = message.reply_to_message.text
                    session.commit()
                    await message.reply(trans['greeting']['set_user_leave_msg'])
                    logger.info(f"{message.chat.full_name}: new leave user msg")
                else:
                    await message.reply(trans['global']['errors']['setup'])
                    logger.warning(f"{message.chat.full_name}: setup greeting")
            else:
                await message.reply(trans['global']['errors']['admin'])
                logger.warning(f"{message.chat.full_name}: {message.from_user.full_name} not admin")
        else:
            await message.reply(trans['global']['errors']['no_reply'])
            logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without reply')

    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(
                f"{message.chat.full_name}: {err}")


@dp.message_handler(commands='rmleavemsg')
async def rm_user_leave_msg(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        if message.reply_to_message:
            member = await bot.get_chat_member(chat_id=message.chat.id,
                                               user_id=message.from_user.id)
            if member.status == 'creator' or member.status == 'administrator':
                result = session.query(Chats.setup_is_finished).filter_by(chat_id=message.chat.id).first()
                if result[0]:
                    chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
                    chat.leave_msg = ''
                    session.commit()
                    await message.reply(trans['greeting']['rm_user_leave_msg'])
                    logger.info(f"{message.chat.full_name}: rm leave user msg")
                else:
                    await message.reply(trans['global']['errors']['setup'])
                    logger.warning(f"{message.chat.full_name}: setup greeting")
            else:
                await message.reply(trans['global']['errors']['admin'])
                logger.warning(f"{message.chat.full_name}: {message.from_user.full_name} not admin")
        else:
            await message.reply(trans['global']['errors']['no_reply'])
            logger.warning(f'{message.chat.full_name}: User {message.from_user.full_name} tried to use command without reply')
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(
            f"{message.chat.full_name}: {err}")


@dp.message_handler(content_types='left_chat_member')
async def user_leave_msg(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        chat = session.query(Chats.setup_is_finished, Chats.leave_msg).filter_by(chat_id=message.chat.id).first()
        try:
            if chat[0] and chat[1]:
                await bot.send_message(chat_id=message.chat.id,
                                       reply_to_message_id=message.message_id,
                                       parse_mode='HTML',
                                       text=chat[1])
                logger.info(f"{message.chat.full_name}: User {message.from_user.full_name} left")
        except IndexError:
            pass
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(
            f"{message.chat.full_name}: {err}")


@dp.callback_query_handler(lambda c: c.data == 'captcha_ok')
async def call_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    if trans == 1:
        return
    try:
        kick_jobs[call.message.chat.id][call.from_user.id].remove()

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
        kick_jobs[call.message.chat.id].pop(call.from_user.id)

        logger.info(f"{call.from_user.full_name} is not bot")
    except KeyError as err:
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=trans['greeting']['other_user_err'])
        logger.error(
            f"{call.from_user.full_name}: {err}")

