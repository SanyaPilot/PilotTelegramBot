import telebot
import config
from translation import tw
import googletrans
from googletrans import Translator

bot = telebot.TeleBot(config.token)
translator = Translator()


def tr(message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        words = message.text.split()
        lang_code = words[1]
        result = translator.translate(message.reply_to_message.text, dest=lang_code)

        langs = googletrans.LANGUAGES
        text = '<i>'
        if trans['translate']['tr'] != '':
            text += trans['translate']['tr'].format(src_lang=langs[result.src], dest_lang=langs[lang_code]) + '\n'

        text += 'Translate from <b>' + langs[result.src] + '</b> to <b>' + langs[lang_code] + '</b></i>\n\n' + \
                result.text
        bot.send_message(chat_id=message.chat.id,
                         reply_to_message_id=message.message_id,
                         parse_mode='HTML',
                         text=text)
    except Exception:
        bot.reply_to(message, trans['global']['errors']['default'])
