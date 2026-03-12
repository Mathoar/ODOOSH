from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    pl_entity = fields.Selection(
        selection=[
            ("frais_pei", "FRAIS PEI"),
            ("lpe", "LPE"),
        ],
        string="Entité",
        tracking=True,
    )
    pl_supplier_type = fields.Selection(
        selection=[
            ("direct", "DIRECT"),
            ("indirect", "INDIRECT"),
        ],
        string="Type fournisseur",
        tracking=True,
    )
    pl_charge_category = fields.Selection(
        selection=[
            ("achats", "ACHATS"),
            ("loyers", "LOYERS"),
            ("frais_generaux", "FRAIS GÉNÉRAUX"),
            ("transport", "TRANSPORT"),
            ("salaires", "SALAIRES"),
            ("assurances", "ASSURANCES"),
            ("entretien", "ENTRETIEN"),
            ("marketing", "MARKETING"),
            ("divers", "DIVERS"),
        ],
        string="Catégorie de charge",
        tracking=True,
    )
    pl_pennylane_id = fields.Char(
        string="ID Pennylane",
        copy=False,
        readonly=True,
        help="Identifiant unique du fournisseur dans Pennylane",
    )
    pl_invoice_count = fields.Integer(
        string="Factures Pennylane",
        compute="_compute_pl_invoice_count",
    )

    def _compute_pl_invoice_count(self):
        invoice_model = self.env["pennylane.invoice"]
        for partner in self:
            partner.pl_invoice_count = invoice_model.search_count(
                [("partner_id", "=", partner.id)]
            )
