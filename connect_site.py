import requests
from bs4 import BeautifulSoup

from services_func import get_day_and_month_date, get_magnetic_field, get_pressure, get_temperature, \
    get_humidity, get_weather_state

# Собираем в словарь данные с каждого дня
day_result_data = {}


def connect_site(getloc):
    ''' Подключаемся к сайту и забираем код страницы'''

    # Формируем ссылку
    url = f'https://yandex.ru/pogoda/details?lat={getloc.latitude}&lon={getloc.longitude}&via=ms'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'cookie': 'yandexuid=4203875121658475745; is_gdpr=0; yuidss=4203875121658475745; gdpr=0; _ym_uid=1658475750420300417; mda=0; is_gdpr_b=CLryEBDmfygC; amcuid=8408910891659463576; L=di5Af2QDB11WAFhbUWVMf3xFVkAIWWV6BVowBCMoPU8jDVI+GmMzQQ==.1661532374.15081.33769.85a4740d8fd297f345b45471a86e08e0; yandex_login=info@go-quest.ru; yandex_gid=213; ys=searchextchrome.8-24-9#udn.cDppbmZvQGdvLXF1ZXN0LnJ1#wprid.1663763657524567-14379197275939370647-sas3-0816-dd1-sas-l7-balancer-8080-BAL-7798#c_chck.1439745122; ymex=1973835749.yrts.1658475749#1980341579.yrtsi.1664981579; i=PU71uGpQ4F68BUtZzFi0zTHIAabgXw7NdbHK3pCmY0/gTMBkzzmD5NgfNgVJFOFFwiSe157g2MQY7bH9slRJ1KK5j58=; spravka=dD0xNjY1MDQ4MzM5O2k9MzcuMTEwLjE1NS4xMTQ7RD1BOEU5RDEwNjYxMTlDMkI5MkMyMTREMURFQkEwMjQzNEEzM0RBM0NEREUyMDE2Q0E2RTA2QjJGRDc4NjQ2NUYzQjlCQUM0M0I7dT0xNjY1MDQ4MzM5NTc1MTY1OTI1O2g9NjIzOGI3NDljZDZlMTU3Nzk3NWFhNmU0MmI1NTY0ZDk=; _ym_d=1665223601; _ym_isad=2; Session_id=3:1665327288.5.0.1658563583752:KK20Hw:24.1.2:1|1130000025684501.0.2|1663104172.2590620.2.2:2590620|3:10259439.312596.lNWZp7qx6HIbmrBMAdCL-r0a1sQ; sessionid2=3:1665327288.5.0.1658563583752:KK20Hw:24.1.2:1.499:1|1130000025684501.0.2|1663104172.2590620.2.2:2590620|3:10259439.830768.fakesign0000000000000000000; _yasc=RlZ73AUkvbUoJqXo0vGytPn9fweL7bcLmrouvalu67TGbi6qpaV4Ji7e9aKfmLdV; ys=udn.cDppbmZvQGdvLXF1ZXN0LnJ1#wprid.1665330472305162-8692653707106005398-vla1-1928-vla-l7-balancer-8080-BAL-6449#c_chck.1031758781; yp=1696863287.p_sw.1665327286#1976892374.udn.cDppbmZvQGdvLXF1ZXN0LnJ1#1976514203.multib.1#1980690473.pcs.0#1665731420.ygu.1#1696518027.pgp.1_27749692#1665586375.mcv.2#1665586375.mcl.19z921t#1665586375.szm.1:1600x900:1600x757; yabs-frequency=/5/3W0209muFsDbt25Z/lG_y8mz9wNdWI2FkZ9N-eSoLPE188sqGN3wa_IrJu4X1IkQnfDqwfKQmI4vZIlIyL2gUUE188000/; cycada=f5xOEeGwEMMkc8brtZZ0safOjcxzlLtGCfvXUjCivjo=',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36:'
    }

    response = requests.get(url=url, headers=headers)  # Создаём запрос
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
