from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # --- Champs clients ---
    x_groupe_client = fields.Selection([
        ('gbh', 'GBH'),
        ('smdis', 'SMDIS'),
        ('cellule_u', 'Cellule U'),
        ('caille', 'Caillé'),
        ('distrimascareignes', 'Distrimascareignes'),
        ('ibl', 'IBL'),
        ('tk', 'TK'),
        ('lot', 'LOT'),
        ('gms', 'GMS'),
        ('autres', 'Autres'),
    ], string='Groupe client')

    x_enseigne = fields.Selection([
        ('auchan', 'Auchan'),
        ('carrefour', 'Carrefour'),
        ('carrefour_market', 'Carrefour Market'),
        ('carrefour_city', 'Carrefour City'),
        ('promocash', 'Promocash'),
        ('u', 'U'),
        ('leclerc', 'Leclerc'),
        ('intermark', 'Intermark'),
        ('run_market', 'Run Market'),
        ('cocci_market', 'Cocci Market'),
        ('leader_price', 'Leader Price'),
        ('gel_oi', 'Gel OI'),
        ('independant', 'Indépendant'),
    ], string='Enseigne')

    x_taux_remise = fields.Float(string='Taux de remise (%)')
    x_taux_rfa = fields.Float(string='Taux RFA (%)')

    x_blocage = fields.Selection([
        ('non', 'Non'),
        ('oui_toujours', 'Oui - Toujours'),
        ('oui_depassement', 'Oui - Dépassement encours'),
    ], string='Blocage', default='non')

    x_compte_comptable = fields.Char(string='N° compte comptable')
    x_responsable_1 = fields.Char(string='Responsable 1')
    x_responsable_2 = fields.Char(string='Responsable 2')
    x_resp_compta = fields.Char(string='Responsable comptabilité')
    x_tel_compta = fields.Char(string='Tél. comptabilité')
    x_email_compta = fields.Char(string='Email comptabilité')
    x_groupe_facturation = fields.Char(string='Groupe facturation')

    # --- Champs fournisseurs ---
    x_nom_commercial = fields.Char(string='Nom commercial')

    x_groupe_fournisseur = fields.Selection([
        ('asie_inde', 'Asie / Inde'),
        ('europe', 'Europe'),
        ('local', 'Local'),
        ('afrique', 'Afrique'),
        ('amerique', 'Amérique'),
        ('oceanie', 'Océanie'),
        ('autres', 'Autres'),
    ], string='Groupe fournisseur')

    x_code_interne = fields.Char(string='Code interne')
    x_compte_auxiliaire = fields.Char(string='Compte auxiliaire')
    x_is_transitaire = fields.Boolean(string='Est transitaire', default=False)
    x_delai_livraison = fields.Integer(string='Délai de livraison (jours)')
    x_incoterm = fields.Char(string='Conditions de livraison')
    x_conditions_achat = fields.Char(string='Conditions d\'achat')
    x_numero_client_chez_frs = fields.Char(string='N° client chez fournisseur')
