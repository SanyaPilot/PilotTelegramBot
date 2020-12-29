from aiogram.types import Message
from init import dp, tw
import googletrans
from googletrans import Translator
from loguru import logger

translator = Translator()


@dp.message_handler(commands='tr')
async def tr(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        words = message.text.split()
        lang_code = words[1]
        result = translator.translate(text=message.reply_to_message.text, dest=lang_code)

        langs = googletrans.LANGUAGES
        text = '<i>'
        if trans['translate']['tr'] != '':
            text += trans['translate']['tr'].format(src_lang=langs[result.src], dest_lang=langs[lang_code]) + '\n'

        text += 'Translate from <b>' + langs[result.src] + '</b> to <b>' + langs[lang_code] + '</b></i>\n\n' + \
                result.text
        await message.reply(text=text, parse_mode='HTML')
        logger.info(f"{message.chat.full_name}: {message.from_user.full_name} - tr")
    except Exception as err:
        await message.reply(trans['global']['errors']['default'])
        logger.error(f"{message.chat.full_name}: User {message.from_user.full_name} {err}")
