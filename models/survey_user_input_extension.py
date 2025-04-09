# -*- coding: utf-8 -*-
from odoo import api, fields, models
import textwrap


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

    aggregated_response = fields.Text(
        string="Réponses Complètes",
        compute="_compute_aggregated_response",
        help="Agrégation de toutes les réponses complètes de la participation."
    )

    def _compute_aggregated_response(self):
        for rec in self:
            full_texts = []
            for line in rec.user_input_line_ids:
                if not line.skipped:
                    question_label = line.question_id.title or ''
                    answer = line.full_answer.strip() or 'N/A'
                    # Diviser la réponse en segments en cas de sauts de ligne existants
                    segments = answer.splitlines()
                    # Reformater chaque segment à une largeur maximale de 90 caractères
                    wrapped_segments = [textwrap.fill(segment, width=90) for segment in segments]
                    # Reconstituer la réponse avec les segments reformattés
                    answer = "\n".join(wrapped_segments)
                    full_texts.append(f"<h5>{question_label}</h5>{answer}")
            rec.aggregated_response = "\n\n".join(full_texts)

    def open_survey_response(self):
        """Méthode pour ouvrir directement le formulaire de réponse détaillé,
           qui affiche l'agrégation complète des réponses."""
        self.ensure_one()
        return {
            'name': 'Détails de la participation',
            'type': 'ir.actions.act_window',
            'res_model': 'survey.user_input',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    full_answer = fields.Text(
        string="Réponse Complète",
        compute="_compute_full_answer",
        store=False
    )

    def _compute_full_answer(self):
        for line in self:
            if line.answer_type == 'char_box':
                line.full_answer = line.value_char_box or ''
            elif line.answer_type == 'text_box':
                line.full_answer = line.value_text_box or ''
            elif line.answer_type == 'numerical_box':
                line.full_answer = str(line.value_numerical_box) if line.value_numerical_box is not None else ''
            elif line.answer_type == 'scale':
                line.full_answer = str(line.value_scale) if line.value_scale is not None else ''
            elif line.answer_type == 'date':
                line.full_answer = fields.Date.to_string(line.value_date) if line.value_date else ''
            elif line.answer_type == 'datetime':
                line.full_answer = fields.Datetime.to_string(line.value_datetime) if line.value_datetime else ''
            elif line.answer_type == 'suggestion':
                if line.matrix_row_id:
                    line.full_answer = f"{line.suggested_answer_id.value}: {line.matrix_row_id.value}"
                else:
                    line.full_answer = line.suggested_answer_id.value or ''
            else:
                line.full_answer = ''