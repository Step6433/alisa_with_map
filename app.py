
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
        res['response']['text'] = f'{cities[0]} находится в стране — {country}'
    elif len(cities) == 2:
        coords_1 = get_geo_info(cities[0], 'coordinates')  # Получение координат первого города
        coords_2 = get_geo_info(cities[1], 'coordinates')  # Получение координат второго города
        distance = get_distance(coords_1, coords_2)
        res['response']['text'] = f'Расстояние между {cities[0]} и {cities[1]} составляет примерно {round(distance)} километров.'
    else:
        res['response']['text'] = 'Укажи меньше городов, пожалуйста!'


def get_cities(req):
    cities = []
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.GEO' and 'city' in entity['value'].keys():
            cities.append(entity['value']['city'])
    return cities

if __name__ == '__main__':
    app.run()