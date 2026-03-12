import json
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from ..services.pennylane_api import PennylaneAPI

_logger = logging.getLogger(__name__)


class PennylaneImportWizard(models.TransientModel):
    _name = "pennylane.import.wizard"
    _description = "Assistant d'import Pennylane"

    date_from = fields.Date(string="Du")
    date_to = fields.Date(string="Au")
    import_type = fields.Selection(
        selection=[
            ("supplier", "Factures fournisseurs"),
            ("customer", "Factures clients"),
            ("both", "Les deux"),
        ],
        string="Type de factures",
        default="supplier",
        required=True,
    )

    def _get_api_client(self):
        token = self.env["ir.config_parameter"].sudo().get_param(
            "pennylane_connector.api_token", ""
        )
        if not token:
            raise UserError(_(
                "Aucun token API Pennylane configuré.\n"
                "Allez dans Paramètres > Comptabilité > Pennylane "
                "et renseignez votre token."
            ))
        base_url = self.env["ir.config_parameter"].sudo().get_param(
            "pennylane_connector.api_base_url",
            "https://app.pennylane.com/api/external/v2",
        )
        return PennylaneAPI(token, base_url)

    def action_test_connection(self):
        client = self._get_api_client()
        success, message = client.test_connection()
        if success:
            raise UserError(_("✅ %s") % message)
        else:
            raise UserError(_("❌ %s") % message)

    def action_import(self):
        self.ensure_one()
        client = self._get_api_client()

        batch = self.env["pennylane.import.batch"].create({
            "date_from": self.date_from,
            "date_to": self.date_to,
            "state": "running",
        })

        errors = []
        total_imported = 0
        total_duplicates = 0

        try:
            if self.import_type in ("supplier", "both"):
                imported, dupes, errs = self._import_invoices(
                    client, batch, "supplier",
                )
                total_imported += imported
                total_duplicates += dupes
                errors.extend(errs)

            if self.import_type in ("customer", "both"):
                imported, dupes, errs = self._import_invoices(
                    client, batch, "customer",
                )
                total_imported += imported
                total_duplicates += dupes
                errors.extend(errs)

            batch.write({
                "state": "done",
                "duplicate_count": total_duplicates,
                "error_log": "\n".join(errors) if errors else False,
            })

        except Exception as e:
            batch.write({
                "state": "error",
                "error_log": str(e),
            })
            raise UserError(_("Erreur lors de l'import : %s") % e) from e

        return {
            "type": "ir.actions.act_window",
            "name": _("Factures importées"),
            "res_model": "pennylane.invoice",
            "view_mode": "list,form",
            "domain": [("import_batch_id", "=", batch.id)],
            "context": {"default_import_batch_id": batch.id},
        }

    def _import_invoices(self, client, batch, invoice_type):
        if invoice_type == "supplier":
            raw_invoices = client.fetch_supplier_invoices(
                date_from=self.date_from,
                date_to=self.date_to,
            )
        else:
            raw_invoices = client.fetch_customer_invoices(
                date_from=self.date_from,
                date_to=self.date_to,
            )

        _logger.info("Pennylane: %d %s invoices fetched", len(raw_invoices), invoice_type)

        imported = 0
        duplicates = 0
        errors = []
        invoice_model = self.env["pennylane.invoice"]

        for raw_inv in raw_invoices:
            pl_id = str(raw_inv.get("id", ""))
            if not pl_id:
                continue

            existing = invoice_model.search([("pennylane_id", "=", pl_id)], limit=1)
            if existing:
                duplicates += 1
                continue

            try:
                lines_data = client.fetch_invoice_lines(pl_id, invoice_type)
                partner = self._find_or_create_partner(raw_inv, invoice_type)

                vals = self._prepare_invoice_vals(raw_inv, partner, batch, invoice_type)
                vals["raw_data"] = json.dumps(raw_inv, ensure_ascii=False, default=str)

                invoice = invoice_model.create(vals)

                for seq, line_data in enumerate(lines_data, start=1):
                    self._create_invoice_line(invoice, line_data, seq)

                imported += 1

            except Exception as e:
                msg = f"Erreur facture {pl_id}: {e}"
                _logger.warning(msg)
                errors.append(msg)

        return imported, duplicates, errors

    def _find_or_create_partner(self, raw_inv, invoice_type):
        partner_model = self.env["res.partner"]
        name_field = "supplier_name" if invoice_type == "supplier" else "customer_name"
        id_field = "supplier_id" if invoice_type == "supplier" else "customer_id"

        pl_partner_id = str(raw_inv.get(id_field, ""))
        partner_name = raw_inv.get(name_field, "")

        if pl_partner_id:
            partner = partner_model.search(
                [("pl_pennylane_id", "=", pl_partner_id)], limit=1,
            )
            if partner:
                return partner

        if partner_name:
            partner = partner_model.search(
                [("name", "=ilike", partner_name), ("supplier_rank", ">", 0)],
                limit=1,
            )
            if partner:
                if not partner.pl_pennylane_id and pl_partner_id:
                    partner.pl_pennylane_id = pl_partner_id
                return partner

        return partner_model.create({
            "name": partner_name or f"Fournisseur Pennylane {pl_partner_id}",
            "supplier_rank": 1 if invoice_type == "supplier" else 0,
            "customer_rank": 1 if invoice_type == "customer" else 0,
            "pl_pennylane_id": pl_partner_id,
        })

    def _prepare_invoice_vals(self, raw_inv, partner, batch, invoice_type):
        return {
            "pennylane_id": str(raw_inv.get("id", "")),
            "invoice_number": raw_inv.get("invoice_number", ""),
            "label": raw_inv.get("label", ""),
            "partner_id": partner.id if partner else False,
            "supplier_name": raw_inv.get("supplier_name") or raw_inv.get("customer_name", ""),
            "pennylane_supplier_id": str(
                raw_inv.get("supplier_id") or raw_inv.get("customer_id", "")
            ),
            "issue_date": raw_inv.get("issue_date"),
            "deadline": raw_inv.get("deadline"),
            "created_date": raw_inv.get("created_date"),
            "amount_ht": float(raw_inv.get("amount_eur_excl_taxes") or 0),
            "amount_ttc": float(raw_inv.get("amount_eur") or 0),
            "currency": raw_inv.get("currency", "EUR"),
            "outstanding_balance": float(raw_inv.get("outstanding_balance") or 0),
            "is_paid": raw_inv.get("is_paid", False),
            "source": raw_inv.get("source", ""),
            "state": "new",
            "import_batch_id": batch.id,
        }

    def _create_invoice_line(self, invoice, line_data, seq):
        self.env["pennylane.invoice.line"].create({
            "invoice_id": invoice.id,
            "sequence": seq * 10,
            "description": line_data.get("description") or line_data.get("label", ""),
            "product_name": line_data.get("product_name") or line_data.get("label", ""),
            "quantity": float(line_data.get("quantity") or 1),
            "unit_price": float(
                line_data.get("unit_price")
                or line_data.get("currency_amount_before_tax")
                or line_data.get("amount")
                or 0
            ),
            "amount_ht": float(line_data.get("currency_amount_before_tax") or line_data.get("amount") or 0),
            "tax_rate": float(line_data.get("vat_rate") or line_data.get("tax_rate") or 0),
            "account_code": line_data.get("planitem_number") or line_data.get("account_code", ""),
        })
