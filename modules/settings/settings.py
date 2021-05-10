from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from init import bot, dp, tw, SettingsStates
from loguru import logger

from modules.settings import warns, greeting, notes


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
                         InlineKeyboardButton(text=trans['settings']['greeting'], callback_data='greeting'),
                         InlineKeyboardButton(text=trans['settings']['notes'], callback_data='notes'),
                         InlineKeyboardButton(text=trans['global']['exit'], callback_data='exit'))

            new_message = await message.reply(text=trans['settings']['start'], reply_markup=keyboard)

            async with state.proxy() as data:
                data['msg_id'] = new_message.message_id
                data['msgs_to_del'] = []
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
                         InlineKeyboardButton(text=trans['settings']['greeting'], callback_data='greeting'),
                         InlineKeyboardButton(text=trans['settings']['notes'], callback_data='notes'),
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
