import telebot
from telebot import types
import requests
import json
import time
from geopy.geocoders import Nominatim

bot = telebot.TeleBot('1073948237:AAGKs3HzRBZwBZGkoQ5moJIakWQn39nQtX4')
geolocator = Nominatim(user_agent="sanya_pilot_telegram_bot")

forecasts = {}
weathers = {}


def weather(message):
    try:
        city_name = message.text[9:]
        loc = geolocator.geocode(city_name)
        if loc is None:
            bot.reply_to(message, 'Такой город не найден')
        else:
            weather_message = bot.send_message(chat_id=message.chat.id,
                                                text='Готовлю прогноз погоды для Вас)',
                                                reply_to_message_id=message.message_id)

            global weathers
            weathers[weather_message.message_id] = message.from_user.id

            response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + str(loc.latitude) +
                                    '&lon=' + str(loc.longitude) + '&appid=c1c0032b6ff3be83e44ab641e780fc3d&lang=RU' +
                                    '&units=metric')

            data = json.loads(response.content)
            destination = loc.address.split(',')

            text = '<b><i>Погода в '
            for i in destination:
                if i == destination[0]:
                    text += i
                else:
                    text += ',' + i

            text += '</i></b>\n'
            text += '━━━━━━━━━━━━━━━━━━━━━━━\n'
            text += '<b>Текущая погода</b>\n'
            text += '━━━━━━━━━━━━━━━━━━━━━━━\n'
            text += '<b>' + str(data['current']['temp']) + ' °C <i>' + data['current']['weather'][0]['description'].capitalize() + '</i></b>\n'
            text += '<i>Чувствуется как:</i> <b>' + str(data['current']['feels_like']) + ' °C</b>\n'
            text += '<i>Влажность:</i> <b>' + str(data['current']['humidity']) + '%</b>\n'
            text += '<i>Давление:</i> <b>' + str(data['current']['pressure']) + ' гПа</b>\n'
            text += '<i>Скорость ветра:</i> <b>' + str(data['current']['wind_speed']) + ' м/с</b>\n'
            text += '<i>Облачность:</i> <b>' + str(data['current']['clouds']) + '%</b>\n'
            text += '<i>UV индекс:</i> <b>' + str(data['current']['uvi']) + '</b>\n'

            keyboard = types.InlineKeyboardMarkup()
            key_close = types.InlineKeyboardButton(text='Я прочитал', callback_data='weather_close')
            keyboard.add(key_close)

            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=weather_message.message_id,
                                  text=text,
                                  parse_mode='HTML',
                                  reply_markup=keyboard)

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


def forecast(message):
    try:
        city_name = message.text[9:]
        loc = geolocator.geocode(city_name)
        if loc is None:
            bot.reply_to(message, 'Такой город не найден')
        else:
            forecast_message = bot.send_message(chat_id=message.chat.id,
                                                text='Готовлю прогноз погоды для Вас)',
                                                reply_to_message_id=message.message_id)

            global forecasts
            forecasts[forecast_message.message_id] = []

            response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + str(loc.latitude) +
                                    '&lon=' + str(loc.longitude) + '&appid=c1c0032b6ff3be83e44ab641e780fc3d&lang=RU' +
                                    '&units=metric')

            data = json.loads(response.content)
            destination = loc.address.split(',')

            for i in range(8):
                text = '<b><i>Погода в '
                for j in destination:
                    if j == destination[0]:
                        text += j
                    else:
                        text += ',' + j

                text += '</i></b>\n'
                text += '━━━━━━━━━━━━━━━━━━━━━━━\n'
                text += '<b>Прогноз на ' + time.strftime("%d/%m", time.gmtime(data['daily'][i]['dt'])) + '</b>\n'
                text += '━━━━━━━━━━━━━━━━━━━━━━━\n'
                text += '<b>' + str(data['daily'][i]['temp']['day']) + ' °C <i>' + data['daily'][i]['weather'][0]['description'].capitalize() + '</i></b>\n'
                text += '<i>Мин. температура:</i> <b>' + str(data['daily'][i]['temp']['min']) + ' °C</b>\n'
                text += '<i>Макс. температура:</i> <b>' + str(data['daily'][i]['temp']['max']) + ' °C</b>\n'
                text += '<i>Температура утром:</i> <b>' + str(data['daily'][i]['temp']['morn']) + ' °C</b>\n'
                text += '<i>Температура вечером:</i> <b>' + str(data['daily'][i]['temp']['eve']) + ' °C</b>\n'
                text += '<i>Температура ночью:</i> <b>' + str(data['daily'][i]['temp']['night']) + ' °C</b>\n'
                text += '<i>Влажность:</i> <b>' + str(data['daily'][i]['humidity']) + '%</b>\n'
                text += '<i>Давление:</i> <b>' + str(data['daily'][i]['pressure']) + ' гПа</b>\n'
                text += '<i>Скорость ветра:</i> <b>' + str(data['daily'][i]['wind_speed']) + ' м/с</b>\n'
                text += '<i>Облачность:</i> <b>' + str(data['daily'][i]['clouds']) + '%</b>\n'
                text += '<i>UV индекс:</i> <b>' + str(data['daily'][i]['uvi']) + '</b>'

                forecasts[forecast_message.message_id].append(text)

            forecasts[forecast_message.message_id].append(0)
            forecasts[forecast_message.message_id].append(message.from_user.id)

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            key_prev = types.InlineKeyboardButton(text='<<', callback_data='forecast_prev')
            key_next = types.InlineKeyboardButton(text='>>', callback_data='forecast_next')
            keyboard.add(key_prev, key_next)
            key_close = types.InlineKeyboardButton(text='Я прочитал', callback_data='forecast_close')
            keyboard.add(key_close)

            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=forecast_message.message_id,
                                  text=forecasts[forecast_message.message_id][0],
                                  parse_mode='HTML',
                                  reply_markup=keyboard)

    except Exception:
        bot.reply_to(message, 'Упс... Что-то пошло не так')


def call_handler(call):
    if call.data == 'forecast_prev':
        if call.from_user.id == forecasts[call.message.message_id][9]:
            if not forecasts[call.message.message_id][8] <= 0:
                forecasts[call.message.message_id][8] -= 1
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                key_prev = types.InlineKeyboardButton(text='<<', callback_data='forecast_prev')
                key_next = types.InlineKeyboardButton(text='>>', callback_data='forecast_next')
                keyboard.add(key_prev, key_next)
                key_close = types.InlineKeyboardButton(text='Я прочитал', callback_data='forecast_close')
                keyboard.add(key_close)

                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=forecasts[call.message.message_id][forecasts[call.message.message_id][8]],
                                      parse_mode='HTML',
                                      reply_markup=keyboard)
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Это начало списка')
        else:
            bot.answer_callback_query(callback_query_id=call.id,
                                      text='Нельзя управлять меню прогноза погоды другого пользователя')

    elif call.data == 'forecast_next':
        if call.from_user.id == forecasts[call.message.message_id][9]:
            if not forecasts[call.message.message_id][8] >= 7:
                forecasts[call.message.message_id][8] += 1
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                key_prev = types.InlineKeyboardButton(text='<<', callback_data='forecast_prev')
                key_next = types.InlineKeyboardButton(text='>>', callback_data='forecast_next')
                keyboard.add(key_prev, key_next)
                key_close = types.InlineKeyboardButton(text='Я прочитал', callback_data='forecast_close')
                keyboard.add(key_close)

                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=forecasts[call.message.message_id][forecasts[call.message.message_id][8]],
                                      parse_mode='HTML',
                                      reply_markup=keyboard)
            else:
                bot.answer_callback_query(callback_query_id=call.id,
                                          text='Это конец списка')
        else:
            bot.answer_callback_query(callback_query_id=call.id,
                                      text='Нельзя управлять меню прогноза погоды другого пользователя')

    elif call.data == 'forecast_close':
        if call.from_user.id == forecasts[call.message.message_id][9]:
            forecasts.pop(call.message.message_id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            bot.answer_callback_query(callback_query_id=call.id,
                                      text='Нельзя управлять меню прогноза погоды другого пользователя')

    elif call.data == 'weather_close':
        if call.from_user.id == weathers[call.message.message_id]:
            weathers.pop(call.message.message_id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            bot.answer_callback_query(callback_query_id=call.id,
                                      text='Нельзя управлять меню прогноза погоды другого пользователя')
