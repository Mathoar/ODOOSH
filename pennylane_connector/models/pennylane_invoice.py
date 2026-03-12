from odoo import api, fields, models


class PennylaneInvoice(models.Model):
    _name = "pennylane.invoice"
    _description = "Facture importée depuis Pennylane"
    _order = "issue_date desc, invoice_number desc"
    _rec_name = "display_name"

    # ─── Identification ────────────────────────────────────────────────
    pennylane_id = fields.Char(
        string="ID Pennylane",
        required=True,
        copy=False,
        index=True,
    )
    invoice_number = fields.Char(string="N° Facture", index=True)
    label = fields.Char(string="Libellé")

    # ─── Fournisseur ───────────────────────────────────────────────────
    partner_id = fields.Many2one(
        "res.partner",
        string="Fournisseur",
        index=True,
    )
    supplier_name = fields.Char(string="Nom fournisseur (Pennylane)")
    pennylane_supplier_id = fields.Char(string="ID fournisseur Pennylane")

    # ─── Classification (héritée du fournisseur) ───────────────────────
    entity = fields.Selection(
        related="partner_id.pl_entity",
        string="Entité",
        store=True,
        readonly=False,
    )
    supplier_type = fields.Selection(
        related="partner_id.pl_supplier_type",
        string="Type",
        store=True,
        readonly=False,
    )
    charge_category = fields.Selection(
        related="partner_id.pl_charge_category",
        string="Catégorie de charge",
        store=True,
        readonly=False,
    )

    # ─── Dates ─────────────────────────────────────────────────────────
    issue_date = fields.Date(string="Date facture", index=True)
    deadline = fields.Date(string="Date échéance")
    created_date = fields.Date(string="Date création Pennylane")

    # ─── Montants ──────────────────────────────────────────────────────
    amount_ht = fields.Float(string="Montant HT (€)", digits=(12, 2))
    amount_ttc = fields.Float(string="Montant TTC (€)", digits=(12, 2))
    currency = fields.Char(string="Devise", default="EUR")
    outstanding_balance = fields.Float(string="Reste à payer", digits=(12, 2))

    # ─── Statut ────────────────────────────────────────────────────────
    is_paid = fields.Boolean(string="Payée dans Pennylane")
    state = fields.Selection(
        selection=[
            ("new", "Nouveau"),
            ("sent", "Envoyé"),
            ("validated", "Validé"),
            ("ignored", "Ignoré"),
        ],
        string="Statut",
        default="new",
        required=True,
        tracking=True,
        index=True,
    )

    # ─── Lien Odoo ─────────────────────────────────────────────────────
    odoo_invoice_id = fields.Many2one(
        "account.move",
        string="Facture Odoo",
        copy=False,
    )

    # ─── Import ────────────────────────────────────────────────────────
    import_batch_id = fields.Many2one(
        "pennylane.import.batch",
        string="Lot d'import",
        ondelete="set null",
    )
    source = fields.Char(string="Source Pennylane")
    raw_data = fields.Text(string="Données brutes JSON")

    # ─── Lignes ────────────────────────────────────────────────────────
    line_ids = fields.One2many(
        "pennylane.invoice.line",
        "invoice_id",
        string="Lignes de facture",
    )

    display_name = fields.Char(compute="_compute_display_name", store=True)

    _sql_constraints = [
        (
            "pennylane_id_unique",
            "UNIQUE(pennylane_id)",
            "Cette facture Pennylane a déjà été importée.",
        ),
    ]

    @api.depends("invoice_number", "supplier_name")
    def _compute_display_name(self):
        for rec in self:
            parts = [rec.invoice_number or "", rec.supplier_name or ""]
            rec.display_name = " - ".join(p for p in parts if p) or f"PL-{rec.pennylane_id}"

    def action_mark_sent(self):
        self.filtered(lambda r: r.state == "new").write({"state": "sent"})

    def action_mark_validated(self):
        self.filtered(lambda r: r.state in ("new", "sent")).write({"state": "validated"})

    def action_mark_ignored(self):
        self.write({"state": "ignored"})

    def action_reset_new(self):
        self.write({"state": "new"})


class PennylaneInvoiceLine(models.Model):
    _name = "pennylane.invoice.line"
    _description = "Ligne de facture Pennylane"
    _order = "sequence, id"

    invoice_id = fields.Many2one(
        "pennylane.invoice",
        string="Facture",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(default=10)
    description = fields.Char(string="Description")
    product_name = fields.Char(string="Produit")
    quantity = fields.Float(string="Quantité", default=1.0, digits=(12, 2))
    unit_price = fields.Float(string="Prix unitaire", digits=(12, 2))
    amount_ht = fields.Float(string="Montant HT", digits=(12, 2))
    tax_rate = fields.Float(string="Taux TVA (%)", digits=(5, 2))
    account_code = fields.Char(string="Compte comptable")
