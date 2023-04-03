from flask import Flask, request, jsonify
import logging
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

musicdata = {}

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
        res['response']['text'] = 'Привет! Что-то интересует?'
        res['response']['text'] = 'Я могу помочь с подбором музыкальных исполнителей или альбомов на твой вкус!'
        res['response']['text'] = 'Ну так что, альбомы или исполнители?'
        sessionStorage[user_id] = {
            'game_started': False
        }
        return

    res['response']['buttons'] = [
        {
            'title': 'Альбомы',
            'hide': True
        },
        {
            'title': 'Исполнители',
            'hide': True
        }
    ]
    if 'альбомы' in req['request']['nlu']['tokens'] or 'исполнители' in req['request']['nlu']['tokens']:
        category = req['request']['nlu']['tokens']
        res['response']['text'] = 'Ну что ж, какую музыку предпочитаешь?'
        if category == 'исполнители':
            musicians(res, req)
        else:
            pass
    else:
        res['response']['text'] = 'Не поняла ответа! Так альбомы или исполнители?'
        res['response']['buttons'] = [
            {
                'title': 'Альбомы',
                'hide': True
            },
            {
                'title': 'Исполнители',
                'hide': True
            }
        ]


def musicians(res, req):
    pass


if __name__ == '__main__':
    app.run()









