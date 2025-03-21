# -*- coding: utf-8 -*-
{
    'name': "CRM Feedback Survey",
    'version': '16.0.1.0.0',
    'author': "Adridot",
    'license': "LGPL-3",
    'category': 'CRM',
    'summary': "Intègre les sondages de feedback dans le CRM, avec sélection du sondage et affichage des participations.",
    'depends': ['crm', 'survey'],
    'data': [
        'views/crm_lead_feedback_views.xml',
        'views/res_config_settings_views.xml',
        'views/survey_user_input_views.xml'
    ],
    'installable': True,
    'application': False,
}