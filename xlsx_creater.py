import xlsxwriter
from geopy import Nominatim

from db import create_table, create_log, connecting_bd
from connect_site import connect_site, get_all_data
import os

# Создаём таблицу
x_file = xlsxwriter.Workbook('result.xlsx')
page = x_file.add_worksheet()

# Добавляем ширину столбцов
page.set_column('A:A', 13)
page.set_column('B:B', 20)
page.set_column('C:C', 20)
page.set_column('D:D', 13)
page.set_column('E:E', 13)
page.set_column('F:F', 25)

# Добавляем стили ячеек
cell_format_blue = x_file.add_format({'bold': True, 'text_wrap': True, 'bg_color': 'fabf8f', 'border': True})
cell_format_blue2 = x_file.add_format({'bold': True, 'text_wrap': True, 'bg_color': 'daeef3', 'border': True})
cell_format_border = x_file.add_format({'border': True, 'text_wrap': True, 'align': 'center'})

# Создаём счетчики для расположения строк и столбцов в таблице
row = 0
column = 0


def create_xlsx(day_data, row, column):
    # Разбираем словарь на переменные
    date = day_data['date']
    magnetic_field = day_data['magnetic_field']
    pressure = day_data['pressure']
    temperature = day_data['temperature']
    humidity = day_data['humidity']
    weather_state = day_data['weather_state']

    # Заполняем таблицу
    page.write(row, column, 'Дата', cell_format_blue)
    page.write_string(row + 1, column, date['date'], cell_format_border)
    page.write(row + 2, column + 1, 'Магнитное поле', cell_format_blue2)
    page.write(row + 2, column + 2, magnetic_field['magnetic_field'], cell_format_border)
    page.write(row + 4, column + 1, 'Давление (предупреждение)', cell_format_blue2)
    page.write(row + 6, column + 1, 'Погода', cell_format_blue2)
    page.write(row + 7, column + 1, 'Время суток:', cell_format_blue2)

    page.write(row + 7, column + 2, 'Температура, °C', cell_format_blue2)
    page.write(row + 8, column + 2, '...'.join(map(str, temperature['morning'])), cell_format_border)
    page.write(row + 9, column + 2, '...'.join(map(str, temperature['day'])), cell_format_border)
    page.write(row + 10, column + 2, '...'.join(map(str, temperature['evening'])), cell_format_border)
    page.write(row + 11, column + 2, '...'.join(map(str, temperature['night'])), cell_format_border)

    page.write(row + 7, column + 3, 'Давление', cell_format_blue2)
    page.write(row + 8, column + 3, pressure['morning'], cell_format_border)
    page.write(row + 9, column + 3, pressure['day'], cell_format_border)
    page.write(row + 10, column + 3, pressure['evening'], cell_format_border)
    page.write(row + 11, column + 3, pressure['night'], cell_format_border)
    page.write(row + 4, column + 2, pressure['warning'], cell_format_border)

    page.write(row + 7, column + 4, 'Влажность', cell_format_blue2)
    page.write(row + 8, column + 4, humidity['morning'], cell_format_border)
    page.write(row + 9, column + 4, humidity['day'], cell_format_border)
    page.write(row + 10, column + 4, humidity['evening'], cell_format_border)
    page.write(row + 11, column + 4, humidity['night'], cell_format_border)

    page.write(row + 7, column + 5, 'Погодное явление', cell_format_blue2)
    page.write(row + 8, column + 5, weather_state['morning'], cell_format_border)
    page.write(row + 9, column + 5, weather_state['day'], cell_format_border)
    page.write(row + 10, column + 5, weather_state['evening'], cell_format_border)
    page.write(row + 11, column + 5, weather_state['night'], cell_format_border)

    page.write(row + 8, column + 1, 'Утро', cell_format_border)
    page.write(row + 9, column + 1, 'День', cell_format_border)
    page.write(row + 10, column + 1, 'Вечер', cell_format_border)
    page.write(row + 11, column + 1, 'Ночь', cell_format_border)

    page.write(row + 13, column + 1, 'Средняя температура за световой день:', cell_format_blue2)
    page.write(row + 13, column + 2, temperature['average'], cell_format_border)


if __name__ == "__main__":

    # Получаем геолокацию города
    city = input('Введите название города: ')
    loc = Nominatim(user_agent='GetLoc')
    getloc = loc.geocode(city)

    db = connecting_bd()  # Подключаемся к БД
    cursor = db.cursor()

    create_table(db, cursor)  # Создаём таблицу в БД

    try:
        start_connect = connect_site(getloc)  # Передаём геолокацию города и забираем страницу
        generator_data = get_all_data(start_connect)  # Генератор с информацией по каждому дню
        for one_day in generator_data:
            create_xlsx(one_day, row, column)  # Заполняем таблицу
            row += 17  # Смещаем начало таблицы на 17 строк вниз

        x_file.close()  # Закрываем таблицу

        create_log(db, cursor, city, "Done")  # Запись в БД
        os.startfile('result.xlsx')

    except Exception as exc:
        print(f'[INFO] - Ошибка: {exc}')
        create_log(db, cursor, city, "Error")  # Запись в БД
