# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_survey_id = fields.Many2one(
        'survey.survey',
        string="Sondage par défaut",
        help="Sondage utilisé par défaut dans les fiches CRM.",
        default_model="crm.lead"
    )

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'crm_feedback_survey.default_feedback_survey_id',
            self.default_survey_id.id or False
        )
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        param = self.env['ir.config_parameter'].sudo()
        survey_id = param.get_param('crm_feedback_survey.default_feedback_survey_id')
        res.update({
            'default_survey_id': int(survey_id) if survey_id and survey_id.isdigit() else False,
        })
        return res