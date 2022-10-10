''' Тут хранятся все функции для обработки html страницы '''


def get_day_and_month_date(html):
    ''' Формируем список даты '''

    day = html.find('strong', class_='forecast-details__day-number').text
    month = html.find('span', class_='forecast-details__day-month').text
    result_date = f'{day} {month}'
    return {'date': result_date}


def get_magnetic_field(html):
    ''' Данные магнитного поля есть только на сегодня и + 3 дня вперёд '''

    # Забираем данные о магнитном поле
    magnetic_field = html.find_all('dd', class_='forecast-fields__value')

    # Взято с https://yandex.ru/pogoda/docs/glossary.html
    all_magnetic_field = ['спокойное', 'неустойчивое', 'слабо возмущенное',
                          'возмущенное', 'магнитная буря', 'большая магнитная буря']

    # Проверяем на совпадения и добавляем
    if magnetic_field and magnetic_field[-1].text in all_magnetic_field:
        return {'magnetic_field': magnetic_field[-1].text}
    else:
        return {'magnetic_field': ''}


def get_pressure(html):
    ''' Получаем данные о давлении и расчитываем предупреждение '''

    result_pressure = {'morning': 0, 'day': 0, 'evening': 0, 'night': 0, 'warning': ''}  # Шаблон для заполнения
    list_pressure_all = html.find_all('td',
                                      class_='weather-table__body-cell weather-table__body-cell_type_air-pressure')

    list_pressure_int = [int(ell_pressure.text) for ell_pressure in list_pressure_all]  # Список всех значений
    max_pressure = max(list_pressure_int)
    min_pressure = min(list_pressure_int)

    if max_pressure - min_pressure >= 5:  # проверяем есть ли завышение показателя > 5

        # Проверяем, спад или увеличение
        if list_pressure_int.index(max_pressure) > list_pressure_int.index(min_pressure):
            result_pressure['warning'] = "Ожидается резкое увеличение атмосферного давления"
        else:
            result_pressure['warning'] = "Ожидается резкое падение атмосферного давления"

    step = 0
    for ell_pressure in result_pressure:  # проходим по шаблону
        if ell_pressure == 'warning':  # Пропускаем предупреждение
            continue
        else:
            result_pressure[ell_pressure] = list_pressure_int[step]  # добавляем значение
        step += 1

    return result_pressure


def get_temperature(html):
    ''' Получаем температуру, высчитываем среднюю '''

    result_temperature = {'morning': [], 'day': [], 'evening': [], 'night': []}  # Шаблон для заполнения
    all_temperature = html.find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_daypart'
                                                 ' weather-table__body-cell_wrapper')
    average_temp = []  # Список для расчёта ср. температуры

    step = 0
    for time_of_day in result_temperature:  # проходим по ключам в шаблоне

        # Дополнительный цикл используем, чтобы отсечь поле "Ощущается как".
        for ell_temperature in all_temperature[step]:

            # Получаем значения температуры по временам дня
            temp_time_of_day = ell_temperature.find_all('span', class_='temp__value temp__value_with-unit')

            for before_after_temp in temp_time_of_day:  # В прогнозе указана температура "+10...+14", вытаскиваем данные
                if before_after_temp.text[0] == '+':
                    int_temp = int(before_after_temp.text[1:])
                    result_temperature[time_of_day].append(int_temp)
                    if time_of_day != 'night':  # Отсекаем ночную температуру, для подсчёта средней за световой день
                        average_temp.append(int_temp)

                else:
                    int_temp = int(before_after_temp.text[1:]) * -1
                    result_temperature[time_of_day].append(int_temp)
                    if time_of_day != 'night':  # Отсекаем ночную температуру, для подсчёта средней за световой день
                        average_temp.append(int_temp)
        step += 1

    result_temperature['average'] = round(sum(average_temp) / len(average_temp))  # Расчитываем сруднюю температуру
    return result_temperature


def get_humidity(html):
    ''' Получаем влажность '''

    result_humidity = {'morning': 0, 'day': 0, 'evening': 0, 'night': 0}  # Шаблон для заполнения
    all_humidity = html.find_all('td', class_='weather-table__body-cell weather-table__body-cell_type_humidity')

    step = 0
    for time_of_day in result_humidity:
        result_humidity[time_of_day] = int(all_humidity[step].text[:-1])
        step += 1

    return result_humidity


def get_weather_state(html):
    ''' Получаем состояние погоды '''

    result_weather_state = {'morning': '', 'day': '', 'evening': '', 'night': ''}  # Шаблон для заполнения
    all_weather_state = html.find_all('td', 'weather-table__body-cell weather-table__body-cell_type_condition')

    step = 0
    for time_of_day in result_weather_state:
        result_weather_state[time_of_day] = all_weather_state[step].text
        step += 1

    return result_weather_state
