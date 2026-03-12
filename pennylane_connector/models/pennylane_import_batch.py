from odoo import api, fields, models


class PennylaneImportBatch(models.Model):
    _name = "pennylane.import.batch"
    _description = "Lot d'import Pennylane"
    _order = "create_date desc"

    name = fields.Char(
        string="Nom",
        compute="_compute_name",
        store=True,
    )
    date_from = fields.Date(string="Période du")
    date_to = fields.Date(string="Période au")
    import_date = fields.Datetime(
        string="Date d'import",
        default=fields.Datetime.now,
        readonly=True,
    )
    user_id = fields.Many2one(
        "res.users",
        string="Importé par",
        default=lambda self: self.env.user,
        readonly=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Brouillon"),
            ("running", "En cours"),
            ("done", "Terminé"),
            ("error", "Erreur"),
        ],
        string="Statut",
        default="draft",
        readonly=True,
    )
    invoice_ids = fields.One2many(
        "pennylane.invoice",
        "import_batch_id",
        string="Factures importées",
    )
    invoice_count = fields.Integer(
        string="Nb factures",
        compute="_compute_counts",
    )
    new_count = fields.Integer(
        string="Nouvelles",
        compute="_compute_counts",
    )
    duplicate_count = fields.Integer(
        string="Doublons ignorés",
        readonly=True,
        default=0,
    )
    error_log = fields.Text(string="Journal d'erreurs", readonly=True)

    @api.depends("date_from", "date_to", "import_date")
    def _compute_name(self):
        for rec in self:
            parts = ["Import"]
            if rec.date_from:
                parts.append(f"du {rec.date_from}")
            if rec.date_to:
                parts.append(f"au {rec.date_to}")
            if rec.import_date:
                parts.append(f"- {rec.import_date.strftime('%d/%m/%Y %H:%M')}")
            rec.name = " ".join(parts)

    def _compute_counts(self):
        for rec in self:
            rec.invoice_count = len(rec.invoice_ids)
            rec.new_count = len(rec.invoice_ids.filtered(lambda i: i.state == "new"))
