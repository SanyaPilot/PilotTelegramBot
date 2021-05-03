from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from init import bot, dp, tw, Chats, session, WarnStates, SettingsStates
import datetime
from babel.dates import format_timedelta
from utils.timedelta import parse_clear_timedelta
from time import sleep
from loguru import logger


@dp.message_handler(commands='settings')
async def settings(message: Message, state: FSMContext):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        member = await bot.get_chat_member(chat_id=message.chat.id,
                                           user_id=message.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            await SettingsStates.menu.set()
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton(text=trans['settings']['warns'], callback_data='warns'),
                         InlineKeyboardButton(text=trans['global']['exit'], callback_data='exit'))

            async with state.proxy() as data:
                data['msg_id'] = message.message_id
                data['msgs_to_del'] = []

            await message.reply(text=trans['settings']['start'], reply_markup=keyboard)
    except Exception as e:
        logger.error(e)


@dp.callback_query_handler(lambda c: c.data == 'settings_home', state='*')
async def home(call: CallbackQuery):
    trans = tw.get_translation(call)
    if trans == 1:
        return
    try:
        await bot.answer_callback_query(call.id)
        member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                           user_id=call.from_user.id)
        if member.status == 'creator' or member.status == 'administrator':
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton(text=trans['settings']['warns'], callback_data='warns'),
                         InlineKeyboardButton(text=trans['global']['exit'], callback_data='exit'))

            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=trans['settings']['start'], reply_markup=keyboard)
            await SettingsStates.menu.set()
    except Exception as e:
        logger.error(e)


@dp.callback_query_handler(lambda c: c.data == 'exit', state=SettingsStates)
async def menu_exit(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.finish()


async def set_ok(message, msg_id, state):
    trans = tw.get_translation(message)
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    async with state.proxy() as data:
        if data['msgs_to_del']:
            for msg in data['msgs_to_del']:
                await bot.delete_message(msg.chat.id, msg.message_id)

            data['msgs_to_del'] = []

    new_message = await bot.send_message(chat_id=message.chat.id, text=trans['global']['ok'], parse_mode='HTML')
    async with state.proxy() as data:
        data['msg_id'] = new_message.message_id

    sleep(2)
    await warns_menu(message, new_message.message_id)


async def set_ok_call(call, state):
    trans = tw.get_translation(call)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=trans['global']['ok'], parse_mode='HTML')
    async with state.proxy() as data:
        data['msg_id'] = call.message.message_id
    sleep(2)
    await settings_warns(call)


async def warns_menu(message, msg_id):
    trans = tw.get_translation(message)
    if trans == 1:
        return

    chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=trans['settings']['warns_max'].format(chat.max_warns), callback_data='max'))

    if chat.warns_punishment is not None:
        punishment_text = trans['global']['punishments'][chat.warns_punishment]
    else:
        punishment_text = '\u274c'

    keyboard.row(InlineKeyboardButton(text=trans['settings']['warns_punishment'].format(punishment_text),
                                      callback_data='punishment'))

    punishment = session.query(Chats.warns_punishment).filter_by(chat_id=message.chat.id).first()

    if not (punishment[0] is None or punishment[0] == 'kick'):
        if chat.warns_punishment_time is not None:
            time_text = format_timedelta(chat.warns_punishment_time, locale='ru', granularity="seconds", format="short")
        else:
            time_text = '\u274c'
        keyboard.row(InlineKeyboardButton(text=trans['settings']['warns_time'].format(time_text),
                                          callback_data='time'))

    keyboard.row(InlineKeyboardButton(text=trans['global']['back'], callback_data='settings_home'),
                 InlineKeyboardButton(text=trans['global']['exit'], callback_data='exit'))

    await bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id,
                                text=trans['settings']['question'], reply_markup=keyboard)
    await SettingsStates.warns.set()


@dp.callback_query_handler(lambda c: c.data == 'warns', state=SettingsStates.menu)
async def settings_warns(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        await warns_menu(call.message, call.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'max', state=SettingsStates.warns)
async def set_max_warns(call: CallbackQuery, state: FSMContext):
    trans = tw.get_translation(call)
    if trans == 1:
        return
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        message = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=trans['warn']['set_max'])
        async with state.proxy() as data:
            data['msg_id'] = message.message_id

        await WarnStates.set_max.set()


@dp.message_handler(state=WarnStates.set_max)
async def set_max_warns(message: Message, state: FSMContext):
    member = await bot.get_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        if message.text.isdigit():
            chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
            chat.max_warns = int(message.text)
            session.commit()
            async with state.proxy() as data:
                data['msgs_to_del'].append(message)

            await SettingsStates.warns.set()
            async with state.proxy() as data:
                await set_ok(message, data['msg_id'], state)


@dp.callback_query_handler(lambda c: c.data == 'punishment', state=SettingsStates.warns)
async def set_warns_punishment(call: CallbackQuery):
    trans = tw.get_translation(call)
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=trans['global']['punishments']['mute'], callback_data='mute'),
                     InlineKeyboardButton(text=trans['global']['punishments']['kick'], callback_data='kick'),
                     InlineKeyboardButton(text=trans['global']['punishments']['ban'], callback_data='ban'),
                     InlineKeyboardButton(text=trans['global']['punishments']['none'], callback_data='none'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=trans['warn']['set_punishment'], reply_markup=keyboard)
        await WarnStates.set_punishment.set()


@dp.callback_query_handler(state=WarnStates.set_punishment)
async def set_warns_punishment(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
        if not call.data == 'none':
            chat.warns_punishment = call.data
        else:
            chat.warns_punishment = None

        session.commit()
        await SettingsStates.warns.set()
        await set_ok_call(call, state)


@dp.callback_query_handler(lambda c: c.data == 'time', state=SettingsStates.warns)
async def set_warns_time(call: CallbackQuery, state: FSMContext):
    trans = tw.get_translation(call)
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        new_message = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                  text=trans['warn']['set_time'])
        async with state.proxy() as data:
            data['msg_id'] = new_message.message_id

        await WarnStates.set_time.set()


@dp.message_handler(state=WarnStates.set_time)
async def set_warns_time(message: Message, state: FSMContext):
    trans = tw.get_translation(message)
    member = await bot.get_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        duration = await parse_clear_timedelta(message)
        if not duration:
            return

        async with state.proxy() as data:
            data['msgs_to_del'].append(message)

        chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
        if not message.text == 'none':
            if duration != datetime.timedelta(hours=999999):
                if not duration < datetime.timedelta(seconds=30):
                    chat.warns_punishment_time = duration.total_seconds()
                else:
                    msg = await message.reply(trans['warn']['time_too_small'])
                    async with state.proxy() as data:
                        data['msgs_to_del'].append(msg)
                    return
            else:
                return
        else:
            chat.warns_punishment_time = None

        session.commit()
        await SettingsStates.warns.set()
        async with state.proxy() as data:
            await set_ok(message, data['msg_id'], state)
