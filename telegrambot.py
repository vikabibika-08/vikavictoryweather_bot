import pyowm
import telebot
from pyowm.utils import config as cfg


config = cfg.get_default_config()
config['language'] = 'ru'

owm = pyowm.OWM('cb1c67439cafb9efac7ef14821822512')
bot = telebot.TeleBot("1421140872:AAEXn3UC-KxXWetTaRs2dDmQ7H2d7o9u1M0", parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Введите наименование города/страны")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Наименование города/страны просписывается на русском или на английском языке. \nБот покажет текущую облачность, погоду и информацию о ветре")

@bot.message_handler(content_types=['text'])
def send_weather(message):
    try:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        wind = w.wind()['speed']

        answer = "Сейчас " + w.detailed_status + "\n"
        answer += "Температура: " + str(temp) + "\n"


        if wind < 5:
            answer += "Слабый ветер \n\n"
        elif wind < 14:
            answer += "Есть ветерок \n\n"
        elif temp < 10 and wind > 14:
            answer += "Метель :(( \n\n"
        elif wind < 25:
            answer += "Сильный ветер \n\n"
        elif wind <33:
            answer += "Очень сильный ветер \n\n"
        elif wind < 100:
            answer += "Ураган!!! \n\n"


        if temp < -10:
            answer += "Бррр, ужасно холодно"
        elif temp < 4:
            answer += "и так холодно, когда лучше в одеялку и не выходить"
        elif temp < 10 and w.detailed_status == 'небольшой дождь' or w.detailed_status == 'дождь':
            answer += "холодновато и мокро - фю"
        elif temp < 10:
            answer += "и холодновато"
        elif temp < 18:
            answer += " Ох, прохладненько"
        elif temp < 24:
            answer += "Тепло, хорошоо! Отличная погода :3 "
        elif temp <30:
            answer += "Жара!"
        elif temp >= 30:
            answer += "Нереальная жара"

        bot.reply_to(message, answer)

    except Exception:
        answer = "use /start or /help"
        bot.reply_to(message, answer)

bot.polling(none_stop=True)




