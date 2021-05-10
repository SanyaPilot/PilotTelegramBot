from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from init import bot, dp, tw, Chats, session, SettingsStates


@dp.callback_query_handler(lambda c: c.data == 'notes', state=SettingsStates.menu)
async def settings_notes(call: CallbackQuery):
    trans = tw.get_translation(call)
    if trans == 1:
        return

    chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
    keyboard = InlineKeyboardMarkup()

    if not chat.notes_send_type:
        text = '\u2705'
    else:
        text = '\u274c'
    keyboard.add(InlineKeyboardButton(text=trans['settings']['notes_send_type'].format(text), callback_data='send_type'))

    keyboard.row(InlineKeyboardButton(text=trans['global']['back'], callback_data='settings_home'),
                 InlineKeyboardButton(text=trans['global']['exit'], callback_data='exit'))

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=trans['settings']['question'], reply_markup=keyboard)
    await SettingsStates.notes.set()


@dp.callback_query_handler(lambda c: c.data == 'send_type', state=SettingsStates.notes)
async def set_send_type(call: CallbackQuery):
    trans = tw.get_translation(call)
    if trans == 1:
        return

    chat = session.query(Chats).filter_by(chat_id=call.message.chat.id).first()
    keyboard = InlineKeyboardMarkup()

    if not chat.notes_send_type:
        chat.notes_send_type = True
        text = '\u274c'
    else:
        chat.notes_send_type = False
        text = '\u2705'

    session.commit()
    keyboard.add(
        InlineKeyboardButton(text=trans['settings']['notes_send_type'].format(text), callback_data='send_type'))

    keyboard.row(InlineKeyboardButton(text=trans['global']['back'], callback_data='settings_home'),
                 InlineKeyboardButton(text=trans['global']['exit'], callback_data='exit'))

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=trans['settings']['question'], reply_markup=keyboard)
