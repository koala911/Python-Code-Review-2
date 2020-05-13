from Parametrs import *
from Parser import WeatherParser
from DrawForecast import DrawForecast


class UsersRequest:
    def __init__(self):
        self.parser = WeatherParser()
        self.answer = ''
        self.requesting_picture = False
        self.draw_forecast = DrawForecast()
    
    def get_answer(self, text):
        self.answer = ''
        self.requesting_picture = False
        users_message = text.lower().strip().split()[:3]

        if len(users_message) == 0:
            self.answer = UNCLEAR
        elif len(users_message) == 1:
            self.handle_one_word(users_message)
        elif len(users_message) == 2:
            self.handle_two_words(users_message)
        elif len(users_message) == 3:
            self.handle_three_words(users_message)

        return self.answer, self.requesting_picture

    def handle_one_word(self, message):
        self.answer = ''
        if message[0] == 'help' or message[0] == 'помощь':
            self.answer = HELP_TEXT
        elif message[0] == 'прогноз':
            forecast = self.parser.get_forecast()
            for i in forecast:
                self.answer += i[0] + ': ' + i[1] + '\n'
            self.requesting_picture = True
            self.draw_forecast.draw(forecast)
        else:
            self.answer = UNCLEAR

    def handle_two_words(self, message):
        self.answer = ''
        if message[0] == 'погода':
            if message[1] == 'сейчас':
                self.answer = self.parser.get_current_temperature()
            elif message[1] == 'сегодня':
                for i in self.parser.get_today_temperature():
                    self.answer += i[0] + ': ' + i[1] + '\n'
            else:
                self.answer = UNCLEAR
        elif message[0] == 'прогноз':
            city = message[1]
            try:
                forecast = self.parser.get_forecast(city)
                for i in forecast:
                    self.answer += i[0] + ': ' + i[1] + '\n'
                if len(self.answer) > 0:
                    self.requesting_picture = True
                    self.draw_forecast.draw(forecast)
            except IndexError:
                self.fix_answer()
        else:
            self.answer = UNCLEAR

        self.fix_answer()

    def handle_three_words(self, message):
        self.answer = ''
        if message[:2] == ['погода', 'сейчас']:
            city = message[2]
            try:
                self.answer = self.parser.get_current_temperature(city)
            except IndexError:
                self.fix_answer()
        elif message[:2] == ['погода', 'сегодня']:
            city = message[2]
            try:
                for i in self.parser.get_today_temperature(city):
                    self.answer += i[0] + ': ' + i[1] + '\n'
            except IndexError:
                self.fix_answer()
        else:
            self.answer = UNCLEAR

        self.fix_answer()

    def fix_answer(self):
        if self.answer == '':
            self.answer = 'Не нашел такого города..\n' + HELP_TEXT
