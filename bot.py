import telebot
import json
import random
from bot_token import token

#load cities
json_file_path = 'cities.json'
with open(json_file_path, 'r', encoding='utf-8') as j:
     cities = json.loads(j.read())['city']

#russian cities
rus_cities = tuple([city['name'].lower() for city in cities if city['country_id'] == '3159'])
city_names = rus_cities

#rare characters
bad_chars = ('ё','ж','й','ф','ц','ш','щ','ъ','ы','ь','э','ю')

#used cities and mistakes count
used = []
mistakes = []

#bot init
bot = telebot.TeleBot('1409701821:AAFEGpBpbof-MqzqcN4bp-ywNUb25MkeHIQ')
#start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет, поиграем в города?")
    bot.send_message(message.chat.id, "Чтобы узнать правила  - отправь /help \nЧтобы окончить игру - отправь /end \nБот ходит первым - Москва. Введи название любого российского города на букву 'а'")
    used.clear()
    used.append('Москва')
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.from_user.id,'Бот и игрок называют российские города по очереди. \nКаждое следующее название города должно начинаться на ту букву, на которую заканчивается предыдущее название. \nУ вас всего три права на ошибку, затем игра будет окончена. \nЕсли в словаре бота закончатся города - победа за вами!')

@bot.message_handler(commands=['end'])
def end(message):
    bot.send_message(message.from_user.id,'Увы, в этот раз победа осталась за мной :) Чтобы начать заново - отправь /start')
    used.clear()          
#game
@bot.message_handler(content_types=['text']) 
def get_text_messages(message): 
    #user input handling
    curr_city = message.text.lower()
    if used:
    #check if first letter meets criteria
        if curr_city[0] != used[-1][-1]:
            #check if number of mistakes exceeds 3
            if len(mistakes) < 3:
                mistakes.append('curr_city')
                bot.send_message(message.chat.id, f'Неверно. Введите город на букву {used[-1][-1]}: ')
            else:
                bot.send_message(message.from_user.id, "Неверно. Игра окончена :( Чтобы начать заново - отправь /start")
                used.clear()
        #response if city is used or unknown  
        elif curr_city in used or curr_city not in city_names:
            bot.send_message(message.from_user.id,'Этот город уже участвовал в игре или такого города еще нет в моем словаре')
        else:
            char = curr_city[-1] if curr_city[-1] not in bad_chars else curr_city[-2]
            next_cities = [name for name in city_names if name.startswith(char) and name not in used]
            if next_cities:
                next_city = random.choice(next_cities)
            else:
                bot.send_message(message.from_user.id, "Победа! :)")
                used.clear()
            used.append(curr_city)
            used.append(next_city)
            bot.send_message(message.from_user.id, next_city.capitalize())
            bot.send_message(message.from_user.id, f'Введите город на букву {used[-1][-1]}: ')
    else:
        bot.send_message(message.from_user.id, 'Чтобы начать игру - отправь /start, чтобы узнать правила - отправь /help')

bot.polling(none_stop=True, interval=0)
