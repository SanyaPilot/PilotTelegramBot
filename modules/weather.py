from init import bot, dp, tw
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import json
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="pilot_telegram_bot")

forecasts = {}
weathers = {}


@dp.message_handler(commands='weather')
async def weather(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        words = message.text.split()
        city_name = words[1]
        loc = geolocator.geocode(city_name)
        if loc is None:
            await bot.reply_to(message, trans['weather']['city_not_found_err'])
        else:
            weather_message = await bot.send_message(chat_id=message.chat.id,
                                                     text=trans['weather']['making_forecast'],
                                                     reply_to_message_id=message.message_id)

            global weathers
            weathers[weather_message.message_id] = message.from_user.id

            response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + str(loc.latitude) +
                                    '&lon=' + str(loc.longitude) + '&appid=c1c0032b6ff3be83e44ab641e780fc3d&lang=' + trans['id'] +
                                    '&units=metric')

            data = json.loads(response.content)
            destination = loc.address.split(',')

            dest = ''
            for i in destination:
                if i == destination[0]:
                    dest += i
                else:
                    dest += ',' + i

            text = trans['weather']['weather_in'].format(city=dest) + '\n'
            text += '━━━━━━━━━━━━━━━━━━━━\n'
            text += trans['weather']['weather']['current_weather'] + '\n'
            text += '━━━━━━━━━━━━━━━━━━━━\n'
            text += '<b>' + str(data['current']['temp']) + ' °C <i>' + data['current']['weather'][0][
                'description'].capitalize() + '</i></b>\n'
            text += trans['weather']['weather']['feels_like'].format(
                feels_like=str(data['current']['feels_like'])) + '\n'
            text += trans['weather']['humidity'].format(humidity=str(data['current']['humidity'])) + '\n'
            text += trans['weather']['pressure'].format(pressure=str(data['current']['pressure'])) + '\n'
            text += trans['weather']['wind_speed'].format(wind_speed=str(data['current']['wind_speed'])) + '\n'
            text += trans['weather']['cloudiness'].format(cloudiness=str(data['current']['clouds'])) + '\n'
            text += trans['weather']['uvi'].format(uvi=str(data['current']['uvi']))

            keyboard = InlineKeyboardMarkup()
            key_close = InlineKeyboardButton(text=trans['weather']['close_button'], callback_data='weather_close')
            keyboard.add(key_close)

            await bot.edit_message_text(chat_id=message.chat.id,
                                        message_id=weather_message.message_id,
                                        text=text,
                                        parse_mode='HTML',
                                        reply_markup=keyboard)

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.message_handler(commands='forecast')
async def forecast(message: Message):
    trans = tw.get_translation(message)
    if trans == 1:
        return
    try:
        words = message.text.split()
        city_name = words[1]
        loc = geolocator.geocode(city_name)
        if loc is None:
            await bot.reply_to(message, trans['weather']['city_not_found_err'])
        else:
            forecast_message = await bot.send_message(chat_id=message.chat.id,
                                                      text=trans['weather']['making_forecast'],
                                                      reply_to_message_id=message.message_id)

            global forecasts
            forecasts[forecast_message.message_id] = []

            response = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=' + str(loc.latitude) +
                                    '&lon=' + str(loc.longitude) + '&appid=c1c0032b6ff3be83e44ab641e780fc3d&lang=' + trans['id'] +
                                    '&units=metric')

            data = json.loads(response.content)
            destination = loc.address.split(',')

            for i in range(8):
                dest = ''
                for j in destination:
                    if j == destination[0]:
                        dest += j
                    else:
                        dest += ',' + j

                text = trans['weather']['weather_in'].format(city=dest) + '\n'
                text += '━━━━━━━━━━━━━━━━━━━━\n'
                text += trans['weather']['forecast']['forecast_for'].format(time=time.strftime("%d/%m", time.gmtime(data['daily'][i]['dt']))) + '\n'
                text += '━━━━━━━━━━━━━━━━━━━━\n'
                text += '<b>' + str(data['daily'][i]['temp']['day']) + ' °C <i>' + data['daily'][i]['weather'][0][
                    'description'].capitalize() + '</i></b>\n'
                text += trans['weather']['forecast']['min_temp'].format(
                    min_temp=str(data['daily'][i]['temp']['min']))+'\n'
                text += trans['weather']['forecast']['max_temp'].format(
                    max_temp=str(data['daily'][i]['temp']['max']))+'\n'
                text += trans['weather']['forecast']['morn_temp'].format(
                    morn_temp=str(data['daily'][i]['temp']['morn']))+'\n'
                text += trans['weather']['forecast']['eve_temp'].format(
                    eve_temp=str(data['daily'][i]['temp']['eve']))+'\n'
                text += trans['weather']['forecast']['night_temp'].format(
                    night_temp=str(data['daily'][i]['temp']['night']))+'\n'
                text += trans['weather']['humidity'].format(humidity=str(data['current']['humidity'])) + '\n'
                text += trans['weather']['pressure'].format(pressure=str(data['current']['pressure'])) + '\n'
                text += trans['weather']['wind_speed'].format(wind_speed=str(data['current']['wind_speed'])) + '\n'
                text += trans['weather']['cloudiness'].format(cloudiness=str(data['current']['clouds'])) + '\n'
                text += trans['weather']['uvi'].format(uvi=str(data['current']['uvi']))

                forecasts[forecast_message.message_id].append(text)

            forecasts[forecast_message.message_id].append(0)
            forecasts[forecast_message.message_id].append(message.from_user.id)

            keyboard = InlineKeyboardMarkup(row_width=2)
            key_prev = InlineKeyboardButton(text='<<', callback_data='forecast_prev')
            key_next = InlineKeyboardButton(text='>>', callback_data='forecast_next')
            keyboard.add(key_prev, key_next)
            key_close = InlineKeyboardButton(text=trans['weather']['close_button'],
                                             callback_data='forecast_close')
            keyboard.add(key_close)

            await bot.edit_message_text(chat_id=message.chat.id,
                                        message_id=forecast_message.message_id,
                                        text=forecasts[forecast_message.message_id][0],
                                        parse_mode='HTML',
                                        reply_markup=keyboard)

    except Exception:
        await message.reply(trans['global']['errors']['default'])


@dp.callback_query_handler(lambda c: 'weather' in c.data or 'forecast' in c.data)
async def call_handler(call):
    trans = tw.get_translation(call)
    if trans == 1:
        return
    if call.data == 'forecast_prev':
        if call.from_user.id == forecasts[call.message.message_id][9]:
            if not forecasts[call.message.message_id][8] <= 0:
                forecasts[call.message.message_id][8] -= 1
                keyboard = InlineKeyboardMarkup(row_width=2)
                key_prev = InlineKeyboardButton(text='<<', callback_data='forecast_prev')
                key_next = InlineKeyboardButton(text='>>', callback_data='forecast_next')
                keyboard.add(key_prev, key_next)
                key_close = InlineKeyboardButton(text=trans['weather']['close_button'],
                                                 callback_data='forecast_close')
                keyboard.add(key_close)

                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=forecasts[call.message.message_id][forecasts[call.message.message_id][8]],
                                            parse_mode='HTML',
                                            reply_markup=keyboard)
            else:
                await bot.answer_callback_query(callback_query_id=call.id,
                                                text=trans['weather']['forecast']['start_of_list'])
        else:
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['weather']['forecast']['other_user_err'])

    elif call.data == 'forecast_next':
        if call.from_user.id == forecasts[call.message.message_id][9]:
            if not forecasts[call.message.message_id][8] >= 7:
                forecasts[call.message.message_id][8] += 1
                keyboard = InlineKeyboardMarkup(row_width=2)
                key_prev = InlineKeyboardButton(text='<<', callback_data='forecast_prev')
                key_next = InlineKeyboardButton(text='>>', callback_data='forecast_next')
                keyboard.add(key_prev, key_next)
                key_close = InlineKeyboardButton(text=trans['weather']['close_button'],
                                                 callback_data='forecast_close')
                keyboard.add(key_close)

                await bot.edit_message_text(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            text=forecasts[call.message.message_id][forecasts[call.message.message_id][8]],
                                            parse_mode='HTML',
                                            reply_markup=keyboard)
            else:
                await bot.answer_callback_query(callback_query_id=call.id,
                                                text=trans['weather']['forecast']['end_of_list'])
        else:
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['weather']['forecast']['other_user_err'])

    elif call.data == 'forecast_close':
        if call.from_user.id == forecasts[call.message.message_id][9]:
            forecasts.pop(call.message.message_id)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['weather']['forecast']['other_user_err'])

    elif call.data == 'weather_close':
        if call.from_user.id == weathers[call.message.message_id]:
            weathers.pop(call.message.message_id)
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text=trans['weather']['forecast']['other_user_err'])
