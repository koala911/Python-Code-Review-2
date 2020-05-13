import unittest
from UsersRequest import UsersRequest
from Parametrs import *


class Test(unittest.TestCase):
    def setUp(self):
        self.users_request = UsersRequest()

    def match_forecast(self, s):
        words = s.split()
        if len(words) != 6:
            return False
        if not words[0].isdigit():
            return False
        if words[2] != 'мин.':
            return False
        if words[4] != 'макс.':
            return False
        return True

    def match_current_weather(self, s):
        words = s.split()
        if len(words) != 2:
            return False
        time = words[0].split(':')
        if len(time) != 3:
            return False
        return time[0].isdigit() and time[1].isdigit()

    def test_handle_one_word(self):
        self.users_request.handle_one_word(["evev"])
        self.assertEqual(self.users_request.answer, UNCLEAR)

        self.users_request.handle_one_word(["help"])
        self.assertEqual(self.users_request.answer, HELP_TEXT)

        self.users_request.handle_one_word(["помощь"])
        self.assertEqual(self.users_request.answer, HELP_TEXT)

        self.users_request.handle_one_word(["прогноз"])
        self.assertTrue(self.users_request.requesting_picture)
        strings = self.users_request.answer.split('\n')
        self.assertEqual(len(strings), 8)
        for i in range(7):
            s = strings[i]
            self.assertTrue(self.match_forecast(s))

    def test_handle_two_words(self):
        self.users_request.handle_two_words(["kjwebf", "woefn"])
        self.assertEqual(self.users_request.answer, UNCLEAR)

        self.users_request.handle_two_words(["погода", "сейчас"])
        self.assertTrue(len(self.users_request.answer) >= 3)

        self.users_request.handle_two_words(["погода", "сегодня"])
        strings = self.users_request.answer.split('\n')
        self.assertEqual(len(strings), 9)
        for i in range(8):
            s = strings[i]
            self.assertTrue(self.match_current_weather(s))

        self.users_request.handle_two_words(["прогноз", "санкт-петербург"])
        self.assertTrue(self.users_request.requesting_picture)
        strings = self.users_request.answer.split('\n')
        self.assertEqual(len(strings), 8)
        for i in range(7):
            s = strings[i]
            self.assertTrue(self.match_forecast(s))

    def test_handle_three_words(self):
        self.users_request.handle_two_words(["погода", "сейчас", "санкт-петербург"])
        self.assertTrue(len(self.users_request.answer) >= 3)

        self.users_request.handle_two_words(["погода", "сегодня", "санкт-петербург"])
        strings = self.users_request.answer.split('\n')
        self.assertEqual(len(strings), 9)
        for i in range(8):
            s = strings[i]
            self.assertTrue(self.match_current_weather(s))

    def test_get_answer(self):
        self.users_request.get_answer("    ПрОгНоЗ    ")
        self.assertTrue(self.users_request.requesting_picture)
        strings = self.users_request.answer.split('\n')
        self.assertEqual(len(strings), 8)
        for i in range(7):
            s = strings[i]
            self.assertTrue(self.match_forecast(s))

        self.users_request.get_answer("    ПогоДа сЕйчас   ")
        self.assertTrue(len(self.users_request.answer) >= 3)

        self.users_request.get_answer("   погоДА СегоднЯ Санкт-петербург     ")
        strings = self.users_request.answer.split('\n')
        self.assertEqual(len(strings), 9)
        for i in range(8):
            s = strings[i]
            self.assertTrue(self.match_current_weather(s))


if __name__ == "__main__":
    unittest.main()
