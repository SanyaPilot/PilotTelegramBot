from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from init import bot, dp, tw, Chats, session, AntispamStates, SettingsStates
from time import sleep
import datetime
from babel.dates import format_timedelta
from utils.timedelta import parse_clear_timedelta


async def antispam_menu(message: Message, msg_id):
    trans = tw.get_translation(message)
    if trans == 1:
        return

    chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=trans['settings']['antispam_max'].format(chat.antispam_max), callback_data='max'))

    if chat.antispam_punishment is not None:
        punishment_text = trans['global']['punishments'][chat.antispam_punishment]
    else:
        punishment_text = '\u274c'

    keyboard.row(InlineKeyboardButton(text=trans['settings']['warns_punishment'].format(punishment_text),
                                      callback_data='punishment'))

    punishment = session.query(Chats.antispam_punishment).filter_by(chat_id=message.chat.id).first()

    if not (punishment[0] is None or punishment[0] == 'kick' or punishment[0] == 'warn'):
        if chat.antispam_punishment_time is not None:
            time_text = format_timedelta(chat.antispam_punishment_time, locale='ru', granularity="seconds", format="short")
        else:
            time_text = '\u274c'
        keyboard.row(InlineKeyboardButton(text=trans['settings']['warns_time'].format(time_text),
                                          callback_data='time'))

    if chat.antispam_can_punish_admins:
        can_punish_admins_text = '\u2705'
    else:
        can_punish_admins_text = '\u274c'

    keyboard.row(InlineKeyboardButton(text=trans['settings']['antispam_punish_admins'].format(can_punish_admins_text),
                                      callback_data='can_punish_admins'))

    keyboard.row(InlineKeyboardButton(text=trans['global']['back'], callback_data='settings_home'),
                 InlineKeyboardButton(text=trans['global']['exit'], callback_data='exit'))

    await bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id,
                                text=trans['settings']['question'], reply_markup=keyboard)
    await SettingsStates.antispam.set()


@dp.callback_query_handler(lambda c: c.data == 'antispam', state=SettingsStates.menu)
async def settings_warns(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        await antispam_menu(call.message, call.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'max', state=SettingsStates.antispam)
async def set_max_warns(call: CallbackQuery, state: FSMContext):
    trans = tw.get_translation(call)
    if trans == 1:
        return
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        message = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=trans['antispam']['set_max'])
        async with state.proxy() as data:
            data['msg_id'] = message.message_id

        await AntispamStates.set_max.set()


@dp.message_handler(state=AntispamStates.set_max)
async def set_max_warns(message: Message, state: FSMContext):
    member = await bot.get_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        if message.text.isdigit():
            chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
            chat.antispam_max = int(message.text)
            session.commit()
            async with state.proxy() as data:
                data['msgs_to_del'].append(message)

            await SettingsStates.antispam.set()
            async with state.proxy() as data:
                await set_ok(message, data['msg_id'], state)


@dp.callback_query_handler(lambda c: c.data == 'punishment', state=SettingsStates.antispam)
async def set_warns_punishment(call: CallbackQuery):
    trans = tw.get_translation(call)
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=trans['global']['punishments']['warn'], callback_data='warn'))
        keyboard.row(InlineKeyboardButton(text=trans['global']['punishments']['mute'], callback_data='mute'),
                     InlineKeyboardButton(text=trans['global']['punishments']['kick'], callback_data='kick'),
                     InlineKeyboardButton(text=trans['global']['punishments']['ban'], callback_data='ban'))
        keyboard.row(InlineKeyboardButton(text=trans['global']['punishments']['none'], callback_data='none'))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=trans['warn']['set_punishment'], reply_markup=keyboard)
        await AntispamStates.set_punishment.set()


@dp.callback_query_handler(state=AntispamStates.set_punishment)
async def set_warns_punishment(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
        if not call.data == 'none':
            chat.antispam_punishment = call.data
        else:
            chat.antispam_punishment = None

        session.commit()
        await SettingsStates.antispam.set()
        await set_ok_call(call, state)


@dp.callback_query_handler(lambda c: c.data == 'time', state=SettingsStates.antispam)
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

        await AntispamStates.set_time.set()


@dp.message_handler(state=AntispamStates.set_time)
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
                    chat.antispam_punishment_time = duration.total_seconds()
                else:
                    msg = await message.reply(trans['warn']['time_too_small'])
                    async with state.proxy() as data:
                        data['msgs_to_del'].append(msg)
                    return
            else:
                return
        else:
            chat.antispam_punishment_time = None

        session.commit()
        await SettingsStates.antispam.set()
        async with state.proxy() as data:
            await set_ok(message, data['msg_id'], state)


@dp.callback_query_handler(lambda c: c.data == 'can_punish_admins', state=SettingsStates.antispam)
async def set_send_type(call: CallbackQuery):
    trans = tw.get_translation(call)
    if trans == 1:
        return

    chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
    keyboard = InlineKeyboardMarkup()

    if chat.antispam_can_punish_admins:
        chat.antispam_can_punish_admins = False
        text = '\u274c'
    else:
        chat.antispam_can_punish_admins = True
        text = '\u2705'

    session.commit()

    await antispam_menu(call.message, call.message.message_id)


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
    await antispam_menu(message, new_message.message_id)


async def set_ok_call(call, state):
    trans = tw.get_translation(call)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=trans['global']['ok'], parse_mode='HTML')
    async with state.proxy() as data:
        data['msg_id'] = call.message.message_id
    sleep(2)
    await settings_warns(call)
