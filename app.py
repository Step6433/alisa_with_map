
from flask import Flask, request
import logging
import json
from geo import get_geo_info, get_distance

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')

@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(response, request.json)

    logging.info('Response: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Я могу сказать в какой стране город или сказать расстояние между городами!'
        return

    cities = get_cities(req)

    if len(cities) == 0:
        res['response']['text'] = 'Ты не указал ни одного города!'
    elif len(cities) == 1:
        country = get_geo_info(cities[0], 'country')  # Используем новую функцию
        res['response']['text'] = f'{cities[0].capitalize()} находится в стране — {country}'
    elif len(cities) == 2:
        coords_1 = get_geo_info(cities[0], 'coordinates')  # Получение координат первого города
        coords_2 = get_geo_info(cities[1], 'coordinates')  # Получение координат второго города
        distance = get_distance(coords_1, coords_2)
        res['response']['text'] = f'Расстояние между {cities[0].capitalize()} и {cities[1].capitalize()} составляет примерно {round(distance)} километров.'
    else:
        res['response']['text'] = 'Укажи меньше городов, пожалуйста!'


# Добавляем расширенное логирование
def get_cities(req):
    cities = []
    entities = req.get('request', {}).get('nlu', {}).get('entities', [])
    logging.info(f'Entities received: {json.dumps(entities, indent=2)}')

    for entity in entities:
        if entity.get('type') == 'YANDEX.GEO':
            value = entity.get('value', {})
            logging.info(f'Processing YANDEX.GEO entity with value: {json.dumps(value, indent=2)}')

            # Проверяем наличие полей с городом различными способами
            city_name = None
            possible_keys = ['city', 'locality', 'geo_object']
            for key in possible_keys:
                if key in value:
                    city_name = value[key]
                    break

            if city_name:
                cities.append(city_name.strip())
                logging.info(f'Added city: {city_name}')
            else:
                logging.warning(f'Skipped entity without valid city name: {entity}')

    return cities

if __name__ == '__main__':
    app.run()