from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_code_interne = fields.Char(string='Code interne')
    x_nom_long = fields.Char(string='Nom long')
    x_contenu = fields.Float(string='Contenu')
    x_conditionnement = fields.Float(string='Conditionnement')
    x_pcb = fields.Float(string='PCB (Par Combien)')
    x_poids_brut = fields.Float(string='Poids brut (kg)')
    x_coef_approche = fields.Float(string='Coefficient d\'approche', default=1.0)
    x_zone_peche = fields.Char(string='Zone de pêche (FAO)')
    x_nom_scientifique = fields.Char(string='Nom scientifique')
    x_origine = fields.Char(string='Origine')
    x_marque = fields.Char(string='Marque')
    x_segment = fields.Char(string='Segment')
    x_taux_om = fields.Float(string='Taux octroi de mer (%)')

    x_pv_ttc = fields.Float(string='PV TTC')
    x_pr_ttc = fields.Float(string='PR TTC')
    x_prmup = fields.Float(string='PRMUP')

    x_tarif_t1_ht = fields.Float(string='Tarif T1 HT')
    x_tarif_t2_ht = fields.Float(string='Tarif T2 HT')
    x_tarif_t3_ht = fields.Float(string='Tarif T3 HT')
    x_tarif_t4_ht = fields.Float(string='Tarif T4 HT')
    x_tarif_t5_ht = fields.Float(string='Tarif T5 HT')
    x_tarif_t6_ht = fields.Float(string='Tarif T6 HT')
