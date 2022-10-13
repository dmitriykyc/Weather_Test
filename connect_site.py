import requests
from bs4 import BeautifulSoup
import browser_cookie3

from services_func import get_day_and_month_date, get_magnetic_field, get_pressure, get_temperature, \
    get_humidity, get_weather_state

# Собираем в словарь данные с каждого дня
day_result_data = {}


def connect_site(getloc):
    ''' Подключаемся к сайту и забираем код страницы'''

    # Формируем ссылку
    url = f'https://yandex.ru/pogoda/details?lat={getloc.latitude}&lon={getloc.longitude}&via=ms'

    # Берём Cookie
    cj = browser_cookie3.chrome()

    response = requests.get(url=url, cookies=cj)  # Создаём запрос
    soup = BeautifulSoup(response.text, features="lxml")

    # Собираем class - 'card' через функцию, чтобы отсечь не точное совпадение, т.к. есть рекламные блоки
    # которые начинаются на 'card .......'
    result_pars = soup.find_all(lambda tag: tag.name == "article" and tag.get('class') == ['card'])

    return result_pars


def get_all_data(data_html):
    ''' Генератор по сбору всей информации в один словарь '''
    for ell in data_html[0:7]:
        # Получаем дату
        date = get_day_and_month_date(ell)
        day_result_data['date'] = date

        # Получаем инфу о магнитном поле
        magnetic_field = get_magnetic_field(ell)
        day_result_data['magnetic_field'] = magnetic_field

        # Получаем информацию о давлении
        pressure = get_pressure(ell)
        day_result_data['pressure'] = pressure

        # Получаем температуру
        temperature = get_temperature(ell)
        day_result_data['temperature'] = temperature

        # Получаем влажность
        humidity = get_humidity(ell)
        day_result_data['humidity'] = humidity

        # Получаем состояние погоды
        weather_state = get_weather_state(ell)
        day_result_data['weather_state'] = weather_state

        yield day_result_data
