import telebot
import googletrans
from googletrans import Translator

bot = telebot.TeleBot('1073948237:AAGKs3HzRBZwBZGkoQ5moJIakWQn39nQtX4')
translator = Translator()


def tr(message):
    try:
        lang_code = message.text[4:]
        result = translator.translate(message.reply_to_message.text, dest=lang_code)

        langs = googletrans.LANGUAGES
        text = '<i>Перевод с <b>' + langs[result.src] + '</b> на <b>' + langs[lang_code] + '</b>\n'
        text += 'Translate from <b>' + langs[result.src] + '</b> to <b>' + langs[
            lang_code] + '</b></i>\n\n' + result.text
        bot.send_message(chat_id=message.chat.id,
                         reply_to_message_id=message.message_id,
                         parse_mode='HTML',
                         text=text)
    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')
