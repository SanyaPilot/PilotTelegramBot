from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from init import bot, dp, tw, Chats, session, GreetingStates, SettingsStates
from time import sleep
from loguru import logger


async def greeting_menu(message, msg_id):
    trans = tw.get_translation(message)
    member = await bot.get_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
        keyboard = InlineKeyboardMarkup()
        if chat.greeting is None:
            symbol = '\u274c'
        else:
            symbol = '\u2705'
        keyboard.add(InlineKeyboardButton(text=trans['settings']['greeting_text'].format(symbol),
                                          callback_data='greeting_text'))

        if chat.leave_msg is None:
            symbol = '\u274c'
        else:
            symbol = '\u2705'
        keyboard.row(InlineKeyboardButton(text=trans['settings']['leave_msg_text'].format(symbol),
                                          callback_data='leave_msg_text'))

        keyboard.row(InlineKeyboardButton(text=trans['global']['back'], callback_data='settings_home'),
                     InlineKeyboardButton(text=trans['global']['exit'], callback_data='exit'))

        await bot.edit_message_text(chat_id=message.chat.id, message_id=msg_id,
                                    text=trans['settings']['question'], reply_markup=keyboard)

        await SettingsStates.greeting.set()


@dp.callback_query_handler(lambda c: c.data == 'greeting', state=SettingsStates.menu)
async def settings_warns(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        await greeting_menu(call.message, call.message.message_id)


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
    await greeting_menu(message, new_message.message_id)


async def show_message(message: Message, state: FSMContext):
    trans = tw.get_translation(message)
    try:
        msg = await message.reply(trans['greeting']['how_it_looks'].format(message.text), parse_mode='HTML')
        async with state.proxy() as data:
            data['msgs_to_del'].append(msg)
        sleep(6)
    except Exception as e:
        msg = await message.reply(trans['greeting']['format_wrong'].format(e))
        async with state.proxy() as data:
            data['msgs_to_del'].append(msg)
        return 1


@dp.callback_query_handler(lambda c: c.data == 'greeting_text', state=SettingsStates.greeting)
async def set_greeting_text(call: CallbackQuery, state: FSMContext):
    trans = tw.get_translation(call)
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        message = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=trans['greeting']['set_greeting'], parse_mode='HTML')
        async with state.proxy() as data:
            data['msg_id'] = message.message_id

        await GreetingStates.set_greeting.set()


@dp.message_handler(state=GreetingStates.set_greeting)
async def set_greeting_text(message: Message, state: FSMContext):
    trans = tw.get_translation(message)
    member = await bot.get_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        bot_obj = await bot.get_me()
        bot_id = bot_obj.id
        me = await bot.get_chat_member(chat_id=message.chat.id, user_id=bot_id)
        if me.can_restrict_members:
            await SettingsStates.greeting.set()
            async with state.proxy() as data:
                data['msgs_to_del'].append(message)

            if not message.text == 'none':
                result = await show_message(message, state)
                if result == 1:
                    await GreetingStates.set_greeting.set()
                    return

            chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
            if message.text == 'none':
                chat.greeting = None
            else:
                chat.greeting = message.text

            session.commit()

            async with state.proxy() as data:
                await set_ok(message, data['msg_id'], state)
            logger.info(f"{message.chat.full_name}: new greeting")

        else:
            perm = 'can_restrict_members'
            await message.reply(trans['global']['errors']['no_needed_perm'].format(perm=perm),
                                parse_mode='HTML')
            logger.warning(f"{message.chat.full_name}: Bot doesn't have perm {perm}")


@dp.callback_query_handler(lambda c: c.data == 'leave_msg_text', state=SettingsStates.greeting)
async def set_leave_msg(call: CallbackQuery, state: FSMContext):
    trans = tw.get_translation(call)
    await bot.answer_callback_query(call.id)
    member = await bot.get_chat_member(chat_id=call.message.chat.id,
                                       user_id=call.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        message = await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              text=trans['greeting']['set_leave_msg'], parse_mode='HTML')
        async with state.proxy() as data:
            data['msg_id'] = message.message_id

        await GreetingStates.set_leave_msg.set()


@dp.message_handler(state=GreetingStates.set_leave_msg)
async def set_leave_msg(message: Message, state: FSMContext):
    member = await bot.get_chat_member(chat_id=message.chat.id,
                                       user_id=message.from_user.id)
    if member.status == 'creator' or member.status == 'administrator':
        await SettingsStates.greeting.set()
        async with state.proxy() as data:
            data['msgs_to_del'].append(message)

        if not message.text == 'none':
            result = await show_message(message, state)
            if result == 1:
                await GreetingStates.set_leave_msg.set()
                return

        chat = session.query(Chats).filter_by(chat_id=message.chat.id).first()
        if message.text == 'none':
            chat.leave_msg = None
        else:
            chat.leave_msg = message.text

        session.commit()

        async with state.proxy() as data:
            await set_ok(message, data['msg_id'], state)
        logger.info(f"{message.chat.full_name}: new greeting")

