# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    survey_id = fields.Many2one(
        'survey.survey',
        string="Sondage",
        default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('crm_feedback_survey.default_feedback_survey_id') or 0),
        help="Sondage à utiliser pour cette opportunité."
    )
    survey_user_input_ids = fields.One2many(
        'survey.user_input',
        'x_lead_id',
        string="Participations au sondage",
        readonly=True,
        help="Liste des participations au sondage liées à cette opportunité."
    )
    survey_user_input_count = fields.Integer(
        string="Nombre de participations",
        compute="_compute_survey_user_input_count"
    )
    show_survey_button = fields.Boolean(
        string="Afficher le bouton de sondage",
        compute="_compute_survey_user_input_count"
    )

    def _compute_survey_user_input_count(self):
        for lead in self:
            lead.survey_user_input_count = self.env['survey.user_input'].search_count([('x_lead_id', '=', lead.id)])
            lead.show_survey_button = lead.survey_user_input_count > 0


    def action_send_survey_link(self):
        """ Méthode déclenchée par le bouton 'Envoyer le formulaire'.
            - Vérifie que le champ survey_id est renseigné.
            - Crée un enregistrement dans survey.user_input en y liant l'opportunité.
            - Appelle l'action standard d'envoi d'invitation du sondage.
        """
        self.ensure_one()
        if not self.survey_id:
            raise UserError("Veuillez sélectionner un sondage pour cette opportunité.")
        # Création de la participation dans survey.user_input
        user_input = self.env['survey.user_input'].create({
            'survey_id': self.survey_id.id,
            'x_lead_id': self.id,
            'email': self.email_from or '',
            'partner_id': self.partner_id.id if self.partner_id else False,
        })
        
        # Préparation du contexte pour inclure le partenaire dans les destinataires
        partners = self.env['res.partner']
        if self.partner_id:
            partners |= self.partner_id
            
        # Appel de l'action standard d'envoi d'invitation avec le contexte approprié
        return self.survey_id.with_context(
            default_existing_mode='new',
            default_partner_ids=partners.ids,
        ).action_send_survey()

    def action_view_survey_user_inputs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Participations au sondage',
            'view_mode': 'tree,form',
            'res_model': 'survey.user_input',
            'domain': [('x_lead_id', '=', self.id)],
            'context': dict(self.env.context, create=False)
        }