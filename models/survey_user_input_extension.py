# -*- coding: utf-8 -*-
from odoo import fields, models

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    x_lead_id = fields.Many2one(
        'crm.lead',
        string="Lead associé",
        help="Fiche CRM à laquelle cette participation est liée."
    )

    partner_ids = fields.Many2many(
        'res.partner', 
        string='Destinataires'
    )

    def open_survey_response(self):
        """Méthode pour ouvrir directement le formulaire de réponse"""
        self.ensure_one()
        return {
            'name': 'Réponse au sondage',
            'type': 'ir.actions.act_window',
            'res_model': 'survey.user_input',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }
    