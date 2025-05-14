import requests
from math import sin, cos, sqrt, atan2, radians


def get_geo_info(city_name, type_info):
    """
    Возвращает информацию о городе (стране или координатах) в зависимости от параметра type_info ('country' or 'coordinates').

    :param city_name: Название города
    :param type_info: Тип запрашиваемой информации ('country' или 'coordinates')
    :return: Страну или координаты в виде tuple (long, lat)
    """
    try:
        # Общий запрос к Yandex Maps API
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            'geocode': city_name,
            'format': 'json'
        }

        response = requests.get(url, params)
        data = response.json()

        # Если нужен country
        if type_info == 'country':
            return data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                'GeocoderMetaData']['AddressDetails']['Country']['CountryName']

        # Если нужны координаты
        elif type_info == 'coordinates':
            coordinates_str = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            long, lat = map(float, coordinates_str.split())
            return long, lat

        else:
            raise ValueError("Некорректный аргумент type_info")

    except Exception as e:
        return f"Произошла ошибка: {e}"


def get_distance(p1, p2):
    """Вычисляет расстояние между двумя точками на Земле"""
    radius = 6373.0

    lon1 = radians(p1[0])
    lat1 = radians(p1[1])
    lon2 = radians(p2[0])
    lat2 = radians(p2[1])

    d_lon = lon2 - lon1
    d_lat = lat2 - lat1

    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = radius * c
    return distance