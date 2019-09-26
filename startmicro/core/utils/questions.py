# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from pprint import pprint

from PyInquirer import style_from_dict, Token, prompt, Separator

style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    # Token.Selected: '',  # default
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options


questions = [
    {
        'type': 'list',
        'name': 'type',
        'message': 'Please choose Microservice type?',
        'choices': [
            'Restful',
            'Redis pubsub',
            'Rabbitmq RPC'
        ]
    },
    {
        'type': 'list',
        'name': 'database',
        'message': 'Please choose Database type?',
        'choices': [
            'No Database',
            'Sqlite',
            'Postgresql',
            'Mysql',
            'MongoDB',
            'Mssql'
        ]
    }
]

