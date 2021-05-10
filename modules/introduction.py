from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ChatType
from aiogram.dispatcher import FSMContext
from init import bot, dp, tw, Chats, session, FirstStartWarnStates
from loguru import logger
from modules.telethon.init import me as telethon_me
from modules.telethon.common import join_chat
from time import sleep
import datetime
from utils.timedelta import parse_clear_timedelta


@dp.message_handler(commands='start')
async def start(message: Message):
    try:
        if message.chat.type == ChatType.SUPERGROUP:
            if not session.query(Chats.chat_id).filter_by(chat_id=message.chat.id).first() == (message.chat.id,):
                new_chat = Chats(chat_id=message.chat.id, helper_in_chat=False, max_warns=5,
                                 warns_punishment='mute', warns_punishment_time=7200, notes_send_type=False,
                                 antispam_max=10, antispam_can_punish_admins=False)
                session.add(new_chat)
                logger.info(f"New chat {message.chat.full_name}")

                keyboard = InlineKeyboardMarkup(row_width=2)
                for i in tw.available:
                    name = i.split('.')[0]
                    keyboard.add(InlineKeyboardButton(text=tw.get_labels()[name], callback_data=f'lang_{name}'))

                if 'eng.json' in tw.available:
                    new_chat.language = 'eng'
                else:
                    new_chat.language = tw.available[0].split('.')[0]

                session.commit()

                trans = tw.get_translation(message)
                try:
                    result = await bot.get_chat_member(chat_id=message.chat.id, user_id=telethon_me.id)
                    if not result.status == 'left' and not result.status == 'kicked':
                        new_chat.helper_in_chat = True
                        session.commit()
                        keyboard.add(
                            InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_finish'))
                    else:
                        keyboard.add(
                            InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_helper'))
                except Exception:
                    keyboard.add(InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_helper'))

                await bot.send_message(message.chat.id, trans['introduction']['start'],
                                       reply_markup=keyboard)
            else:
                logger.warning(f"Non-new chat {message.chat.full_name}")
    except Exception as err:
        logger.error(f"{message.chat.full_name}: {err}")


@dp.message_handler(commands='help')
async def help(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return

    await bot.send_message(chat_id=message.chat.id,
                           text=trans['introduction']['help'])
    logger.info(f"{message.chat.full_name}: {message.from_user.full_name} - {message.text}")


async def finish(call: CallbackQuery):
    trans = tw.get_translation(call)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=trans['introduction']['setup_finished'], parse_mode='HTML')

    # sleep(5)
    # await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


async def finish_from_msg(message: Message):
    trans = tw.get_translation(message)
    # await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
    #                             text=trans['introduction']['setup_finished'], parse_mode='HTML')
    await bot.send_message(chat_id=message.chat.id, text=trans['introduction']['setup_finished'], parse_mode='HTML')
    sleep(5)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@dp.callback_query_handler(lambda c: 'lang' in c.data)
async def call_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    try:
        member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                           user_id=call.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
            chat.language = call.data[5:]
            session.commit()
            trans = tw.get_translation(call)
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['lang_set'])

            keyboard = InlineKeyboardMarkup(row_width=2)
            for i in tw.available:
                name = i.split('.')[0]
                keyboard.add(
                    InlineKeyboardButton(text=tw.get_labels()[name], callback_data=f'lang_{name}'))

            try:
                result = await bot.get_chat_member(chat_id=call.message.chat.id, user_id=telethon_me.id)
                if not result.status == 'left' and not result.status == 'kicked':
                    keyboard.add(InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_warns'))
                else:
                    keyboard.add(InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_warns'))
            except Exception:
                keyboard.add(InlineKeyboardButton(text=trans['introduction']['next'], callback_data='start_warns'))

            await bot.edit_message_text(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        text=trans['introduction']['start'],
                                        reply_markup=keyboard)

        else:
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['global']['errors']['admin'])

    except Exception as err:
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=trans['global']['errors']['default'])
        logger.error(f"{call.message.chat.full_name}: {err}")


#@dp.callback_query_handler(lambda c: c.data == 'start_helper')
async def call_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    try:
        member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                           user_id=call.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=trans['global']['yes'], callback_data='start_helper_join'),
                         InlineKeyboardButton(text=trans['global']['no'], callback_data='start_finish'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=trans['introduction']['add_helper'], reply_markup=keyboard)

    except Exception as err:
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=trans['global']['errors']['default'])
        logger.error(f"{call.message.chat.full_name}: {err}")


async def helper_join_err(call: CallbackQuery):
    trans = tw.get_translation(call)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=trans['introduction']['try_again'], callback_data='start_helper_join'),
                 InlineKeyboardButton(text=trans['introduction']['skip'], callback_data='start_finish'))
    try:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=trans['introduction']['helper_join_failed'], parse_mode='HTML',
                                    reply_markup=keyboard)
    except Exception:
        pass


#@dp.callback_query_handler(lambda c: c.data == 'start_helper_join')
async def callback_handler(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    try:
        await bot.export_chat_invite_link(chat_id=call.message.chat.id)
    except Exception:
        await helper_join_err(call)
        return

    chat = await bot.get_chat(chat_id=call.message.chat.id)
    invite_link = chat.invite_link
    result = await join_chat(call.message.chat.id)
    if not result:
        result = await join_chat(invite_link.split('https://t.me/joinchat/', 1)[1])
        if not result:
            await helper_join_err(call)
            return

    chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
    chat.helper_in_chat = True
    session.commit()
    await finish(call)


@dp.callback_query_handler(lambda c: c.data == 'start_warns')
async def callback_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    try:
        member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                           user_id=call.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            keyboard = InlineKeyboardMarkup().add(
                InlineKeyboardButton(text=trans['global']['yes'], callback_data='start_edit_warns'),
                InlineKeyboardButton(text=trans['global']['no'], callback_data='start_finish'))

            max_warns = session.query(Chats.max_warns).filter_by(chat_id=call.message.chat.id).first()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=trans['introduction']['warns'].format(max_warns=max_warns[0]), reply_markup=keyboard, parse_mode='HTML')
    except Exception as err:
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=trans['global']['errors']['default'])
        logger.error(f"{call.message.chat.full_name}: {err}")


@dp.callback_query_handler(lambda c: c.data == 'start_edit_warns')
async def callback_handler(call: CallbackQuery):
    trans = tw.get_translation(call)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=trans['warn']['set_max'])
        await FirstStartWarnStates.set_max.set()


@dp.message_handler(state=FirstStartWarnStates.set_max)
async def set_max_warns(message: Message, state: FSMContext):
    trans = tw.get_translation(message)
    member = await bot.get_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        if message.text.isdigit():
            chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
            chat.max_warns = int(message.text)
            session.commit()
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text=trans['global']['punishments']['mute'], callback_data='mute'),
                         InlineKeyboardButton(text=trans['global']['punishments']['kick'], callback_data='kick'),
                         InlineKeyboardButton(text=trans['global']['punishments']['ban'], callback_data='ban'),
                         InlineKeyboardButton(text=trans['global']['punishments']['none'], callback_data='none'))
            await bot.send_message(chat_id=message.chat.id, text=trans['warn']['set_punishment'], reply_markup=keyboard)
            await FirstStartWarnStates.next()


@dp.callback_query_handler(state=FirstStartWarnStates.set_punishment)
async def set_punishment(call: CallbackQuery, state: FSMContext):
    trans = tw.get_translation(call)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
        if not call.data == 'none':
            chat.warns_punishment = call.data
            session.commit()

        if call.data == 'mute' or call.data == 'ban':
            await bot.send_message(chat_id=call.message.chat.id, text=trans['warn']['set_time'])
            await FirstStartWarnStates.next()
        else:
            await state.finish()
            await finish(call)


@dp.message_handler(state=FirstStartWarnStates.set_time)
async def set_warns_time(message: Message, state: FSMContext):
    trans = tw.get_translation(message)
    member = await bot.get_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        duration = await parse_clear_timedelta(message)
        if not duration:
            return

        chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
        if not message.text == 'none':
            if duration != datetime.timedelta(hours=999999):
                if not duration < datetime.timedelta(seconds=30):
                    chat.warns_punishment_time = duration.total_seconds()
                else:
                    await message.reply(trans['warn']['time_too_small'])
                    return
            else:
                await message.reply(trans['warn']['time_not_found'])
                return
        else:
            chat.warns_punishment_time = None

        session.commit()
        await state.finish()
        await finish_from_msg(message)
        return


@dp.callback_query_handler(lambda c: c.data == 'start_finish')
async def callback_handler(call: CallbackQuery):
    await finish(call)
