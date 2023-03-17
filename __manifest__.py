# -*- coding: utf-8 -*-
{
    'name': "Todo List GTD",

    'summary': """
        Módulo útil para organizar las actividades de tu empresa según el modelo GTD.""",

    'description': """
        
    """,

    'author': "Enrique Carretero Tato",
    'website': "https://www.iessanclemente.net",

    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'data/recurring.xml',
        'data/general.xml',
        'security/ir.model.access.csv',
        "views/todo_list_enrique.xml"
    ],
}
