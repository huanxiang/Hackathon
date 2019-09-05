from flask_api import FlaskAPI
from config.env import app_env
from app.utils.slackhelper import SlackHelper
from flask import request, jsonify
from app.actions import Actions
from re import match
import requests
import json


allowed_commands = [
    'help', 'search'
]

header = {'Authorization': 'Bearer LPPASVIMTRAJ7TT3AVQNQDJ3W7TXN3CM'}


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=False)
    app.config.from_object(app_env[config_name])
    app.config.from_pyfile('../config/env.py')

    def wit_question(question):
        query = 'https://api.wit.ai/message?v=20190905&q={}'.format(question)
        wit_response = requests.get(query, headers=header).json()
        return wit_response

    @app.route('/swampbot', methods=['POST'])
    def swampbot():
        command_text = request.data.get('text')
        command_text = command_text.split(' ')
        slack_uid = request.data.get('user_id')
        slackhelper = SlackHelper()
        slack_user_info = slackhelper.user_info(slack_uid)
        actions = Actions(slackhelper, slack_user_info)

        question = ''
        for word in command_text:
            question += word + ' '

        response_str = '*You are asking:* \n' + question + '\n\n'

        wit_response = wit_question(question)

        trial_name = wit_response['entities']['clinical_trial'][0]['value']

        url = 'https://api.opentrials.net/v1/search?q=public_title%3A({})&page=1&per_page=10'.format(trial_name)
        api_response = requests.get(url).json()
        response_str += '*Here is what I found:* \n\n'
        for item in api_response['items']:
            response_str += '*id:* \t' + item['id'] + '\n' + '*public_title:* \t' + item['public_title'] + '\n'
            response_str += '*intervention:* \n'
            for drug in item['interventions']:
                response_str += '- ' + drug['name'] + '\n'
            response_str += '-----------------------------------------------------------------------\n'

        response_body = {'text': response_str}

        response = jsonify(response_body)
        response.status_code = 200
        return response

    return app
