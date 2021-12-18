import bs4
import requests


class WeatherParser:
    def __init__(self):
        self.url = "https://sinoptik.com.ru/погода-"

    def get_beautiful_soup(self, city):
        request = requests.get(self.url + city)
        return bs4.BeautifulSoup(request.text, "html.parser")

    def get_current_temperature(self, city='москва'):
        beautiful_soup = self.get_beautiful_soup(city)
        return beautiful_soup.select('.weather__article_main_temp')[0].getText().replace('\n', '')

    def get_forecast(self, city='москва'):
        beautiful_soup = self.get_beautiful_soup(city)
        diapason_list = [
            i.getText().replace('\n\n\n', ' ').replace('\n\n', ' ').replace('\n', '').strip()
            for i in beautiful_soup.select('.weather__content_tab-temperature')
        ]
        date_list = [
            i.getText() for i in beautiful_soup.select('.weather__content_tab-date')
        ]
        month_list = [
            i.getText() for i in beautiful_soup.select('.weather__content_tab-month')
        ]
        result = [
            (i[0] + ' ' + i[1], i[2]) for i in zip(date_list, month_list, diapason_list)
        ]
        return result

    def get_today_temperature(self, city='москва'):
        beautiful_soup = self.get_beautiful_soup(city)
        time_list = [
            i.getText().replace('\n', '')
            for i in beautiful_soup.select('.weather__article_main_right-table .table__time_hours')
        ]
        temperature_list = [
            i.getText()
            for i in beautiful_soup.select('.weather__article_main_right-table .table__temp')
        ]
        result = list(zip(time_list, temperature_list))
        return result
