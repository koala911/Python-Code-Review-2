from Parametrs import *
from Parser import WeatherParser
from DrawForecast import DrawForecast


class UsersRequest:
    def __init__(self):
        self.parser = WeatherParser()
        self.answer = ''
        self.requesting_picture = False
        self.draw_forecast = DrawForecast()
        self.users_city = dict()
    
    def get_answer(self, text, user_id):
        self.answer = ''
        self.requesting_picture = False
        users_message = text.lower().strip().split()

        if len(users_message) == 0:
            self.answer = UNCLEAR
        elif users_message[0] == 'помощь' or users_message[0] == 'help':
            self.handle_help(users_message, user_id)
        elif users_message[0] == 'погода':
            self.handle_today_weather(users_message, user_id)
        elif users_message[0] == 'прогноз':
            self.handle_forecast(users_message, user_id)
        elif users_message[0] == 'город':
            self.handle_set_city(users_message, user_id)
        else:
            self.answer = UNCLEAR

        self.fix_answer()

        return self.answer, self.requesting_picture

    def set_users_city(self, user_id, city):
        self.users_city[user_id] = city

    def handle_forecast(self, message, user_id):
        self.answer = ''
        city = "москва"
        if len(message) == 1:
            if user_id in self.users_city:
                city = self.users_city[user_id]
        else:
            city = '-'.join(message[1:])
        try:
            forecast = self.parser.get_forecast(city)
            for i in forecast:
                self.answer += i[0] + ': ' + i[1] + '\n'
            if len(self.answer) > 0:
                self.requesting_picture = True
                self.draw_forecast.draw(forecast)
        except IndexError:
            self.fix_answer()

    def handle_current_weather(self, message, user_id):
        self.answer = ''
        city = "москва"
        if len(message) == 1:
            if user_id in self.users_city:
                city = self.users_city[user_id]
        elif message[1] == 'сейчас':
            if len(message) > 2:
                city = '-'.join(message[2:])
            else:
                if user_id in self.users_city:
                    city = self.users_city[user_id]
        else:
            city = '-'.join(message[1:])

        try:
            self.answer = self.parser.get_current_temperature(city)
        except IndexError:
            self.fix_answer()

    def handle_today_weather(self, message, user_id):
        self.answer = ''
        city = "москва"
        if len(message) == 1 or message[1] != 'сегодня':
            self.handle_current_weather(message, user_id)
            return
        elif message[1] == 'сегодня':
            if len(message) > 2:
                city = '-'.join(message[2:])
            else:
                if user_id in self.users_city:
                    city = self.users_city[user_id]
        try:
            for i in self.parser.get_today_temperature(city):
                self.answer += i[0] + ': ' + i[1] + '\n'
        except IndexError:
            self.fix_answer()

    def handle_set_city(self, message, user_id):
        self.set_users_city(user_id, '-'.join(message[1:]))
        self.requesting_picture = False
        self.answer = CITY_SET

    def handle_help(self, message, user_id):
        self.answer = HELP_TEXT

    def fix_answer(self):
        if self.answer == '':
            self.answer = 'Не нашел такого города..\n' + HELP_TEXT
