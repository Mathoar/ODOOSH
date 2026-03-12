from odoo import models, fields, api


class MyModel(models.Model):
    _name = 'my.custom.model'
    _description = 'Mon Modèle Personnalisé'

    name = fields.Char(string='Nom', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Actif', default=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('done', 'Terminé'),
    ], string='État', default='draft')

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_reset(self):
        self.write({'state': 'draft'})
