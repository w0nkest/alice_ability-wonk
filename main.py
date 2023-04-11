from flask import Flask, request, jsonify
import logging
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


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
    return jsonify(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови своё имя!'
        sessionStorage[user_id] = {
            'cat_selected': False,
            'first_name': None,
            'genre_selected': False
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            sessionStorage[user_id]['guessed_cities'] = []
            res['response'][
                'text'] = f'''Приятно познакомиться, {first_name.title()}. Я Алиса. 
                        Могу помочь в выборе музыкальных исполнителей и альбомов! 
                        Помочь выбрать альбом или исполнителя?'''
            res['response']['buttons'] = [
                {
                    'title': 'Альбом',
                    'hide': True
                },
                {
                    'title': 'Исполнителя',
                    'hide': True
                }
            ]
    else:
        if not sessionStorage[user_id]['cat_selected']:
            if 'альбом' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['cat_selected'] = True
                albums(res, req)
            elif 'исполнителя' in req['request']['nlu']['tokens']:
                sessionStorage[user_id]['cat_selected'] = True
                musician(res, req)
            else:
                res['response']['text'] = '''Не поняла ответа! Возможно ты написал неверно, попробуй 
                                            "альбом"/"исполнителя"'''
                res['response']['buttons'] = [
                    {
                        'title': 'Альбом',
                        'hide': True
                    },
                    {
                        'title': 'Исполнителя',
                        'hide': True
                    }
                ]
        else:
            albums(res, req)


def albums(res, req):
    user_id = req['session']['user_id']
    if not sessionStorage[user_id]['genre_selected']:
        res['response']['buttons'] = [
            {
                'title': 'Допустимые жанры',
                'hide': True
            }
        ]
        user_id = req['session']['user_id']
        if 'допустимые' in req['request']['nlu']['tokens'] and 'жанры' in req['request']['nlu']['tokens']:
            res['response']['text'] = 'ЖАНРЫ'
        else:
            res['response']['text'] = f"Пора выбрать жанр!"
    else:
        pass


def musician(res, req):
    pass


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    app.run()
