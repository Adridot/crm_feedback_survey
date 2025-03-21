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

    def action_send_survey_link(self):
        """ Méthode déclenchée par le bouton 'Envoyer le formulaire'.
            - Vérifie que le champ survey_id est renseigné.
            - Crée un enregistrement dans survey.user_input en y liant l'opportunité.
            - Appelle l'action standard d'envoi d'invitation du sondage.
        """
        self.ensure_one()
        if not self.survey_id:
            raise UserError(_("Veuillez sélectionner un sondage pour cette opportunité."))
        # Création de la participation dans survey.user_input
        user_input = self.env['survey.user_input'].create({
            'survey_id': self.survey_id.id,
            'x_lead_id': self.id,
            'email': self.email_from or '',
            # Si besoin, on peut générer ou définir un invite_token via la méthode standard
        })
        # Appel de l'action standard d'envoi d'invitation.
        # Celle-ci ouvre le wizard avec le template standard d'invitation.
        return self.survey_id.action_send_survey()