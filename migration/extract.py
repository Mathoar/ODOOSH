"""
Extraction des données Pennylane et transformation au format CSV Odoo.
Usage : python extract.py
"""

import csv
import json
import os
import sys
import time

from config import (
    PENNYLANE_API_TOKEN,
    DATE_FROM,
    DATE_TO,
    EXTRACT_CUSTOMER_INVOICES,
    EXTRACT_SUPPLIER_INVOICES,
    OUTPUT_DIR,
)
from pennylane_client import PennylaneClient


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "raw"), exist_ok=True)


def save_json(data, filename):
    path = os.path.join(OUTPUT_DIR, "raw", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"  💾 Sauvegardé : {path}")


# ─── Extraction brute ─────────────────────────────────────────────────

def extract_customer_invoices(client):
    invoices = client.list_customer_invoices(
        date_from=DATE_FROM or None,
        date_to=DATE_TO or None,
    )
    print(f"  → {len(invoices)} factures clients récupérées")
    save_json(invoices, "customer_invoices.json")

    print("  📄 Récupération des lignes de factures clients...")
    for i, inv in enumerate(invoices):
        inv_id = inv.get("id")
        if not inv_id:
            continue
        try:
            lines = client.get_customer_invoice_lines(inv_id)
            inv["_lines"] = lines
        except Exception as e:
            print(f"    ⚠ Erreur lignes facture {inv_id}: {e}")
            inv["_lines"] = []

        if (i + 1) % 20 == 0:
            print(f"    → {i + 1}/{len(invoices)} factures traitées")
        time.sleep(0.2)

    save_json(invoices, "customer_invoices_with_lines.json")
    return invoices


def extract_supplier_invoices(client):
    invoices = client.list_supplier_invoices(
        date_from=DATE_FROM or None,
        date_to=DATE_TO or None,
    )
    print(f"  → {len(invoices)} factures fournisseurs récupérées")
    save_json(invoices, "supplier_invoices.json")

    print("  📄 Récupération des lignes de factures fournisseurs...")
    for i, inv in enumerate(invoices):
        inv_id = inv.get("id")
        if not inv_id:
            continue
        try:
            lines = client.get_supplier_invoice_lines(inv_id)
            inv["_lines"] = lines
        except Exception as e:
            print(f"    ⚠ Erreur lignes facture {inv_id}: {e}")
            inv["_lines"] = []

        if (i + 1) % 20 == 0:
            print(f"    → {i + 1}/{len(invoices)} factures traitées")
        time.sleep(0.2)

    save_json(invoices, "supplier_invoices_with_lines.json")
    return invoices


# ─── Transformation CSV pour Odoo ─────────────────────────────────────

ODOO_INVOICE_HEADERS = [
    "Numéro",
    "Type",
    "Partenaire",
    "Date facture",
    "Date échéance",
    "Devise",
    "Produit (ligne)",
    "Description (ligne)",
    "Quantité (ligne)",
    "Prix unitaire (ligne)",
    "Taxes (ligne)",
    "Montant HT total",
    "Montant TTC total",
    "Statut paiement",
    "Référence Pennylane",
]


def safe(val, default=""):
    if val is None:
        return default
    return str(val).strip()


def transform_invoices_to_csv(invoices, invoice_type, filename):
    """Transforme les factures Pennylane en CSV importable dans Odoo."""
    path = os.path.join(OUTPUT_DIR, filename)
    rows = []

    for inv in invoices:
        lines = inv.get("_lines") or []
        base_row = {
            "Numéro": safe(inv.get("invoice_number")),
            "Type": invoice_type,
            "Partenaire": safe(
                inv.get("customer_name") or inv.get("supplier_name") or inv.get("label", "")
            ),
            "Date facture": safe(inv.get("issue_date") or inv.get("date")),
            "Date échéance": safe(inv.get("deadline")),
            "Devise": safe(inv.get("currency"), "EUR"),
            "Montant HT total": safe(inv.get("amount_eur_excl_taxes") or inv.get("currency_amount_before_tax")),
            "Montant TTC total": safe(inv.get("amount_eur") or inv.get("currency_amount")),
            "Statut paiement": "Payé" if inv.get("is_paid") else "Non payé",
            "Référence Pennylane": safe(inv.get("id")),
        }

        if lines:
            for line in lines:
                row = dict(base_row)
                row["Produit (ligne)"] = safe(
                    line.get("product_name") or line.get("label") or line.get("description", "")
                )
                row["Description (ligne)"] = safe(
                    line.get("description") or line.get("label", "")
                )
                row["Quantité (ligne)"] = safe(line.get("quantity"), "1")
                row["Prix unitaire (ligne)"] = safe(
                    line.get("unit_price") or line.get("currency_amount_before_tax") or line.get("amount", "")
                )
                tax_rate = line.get("vat_rate") or line.get("tax_rate")
                row["Taxes (ligne)"] = f"{tax_rate}%" if tax_rate else ""
                rows.append(row)
        else:
            base_row["Produit (ligne)"] = ""
            base_row["Description (ligne)"] = safe(inv.get("label", ""))
            base_row["Quantité (ligne)"] = "1"
            base_row["Prix unitaire (ligne)"] = base_row["Montant HT total"]
            base_row["Taxes (ligne)"] = ""
            rows.append(base_row)

    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ODOO_INVOICE_HEADERS, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)

    print(f"  📊 CSV Odoo : {path} ({len(rows)} lignes)")
    return rows


# ─── Rapport résumé ───────────────────────────────────────────────────

def print_summary(customer_invoices, supplier_invoices):
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DE L'EXTRACTION")
    print("=" * 60)

    if customer_invoices:
        total_ht = sum(
            float(inv.get("amount_eur_excl_taxes") or 0)
            for inv in customer_invoices
        )
        total_ttc = sum(
            float(inv.get("amount_eur") or 0)
            for inv in customer_invoices
        )
        paid = sum(1 for inv in customer_invoices if inv.get("is_paid"))
        print(f"\n  Factures clients : {len(customer_invoices)}")
        print(f"    → Total HT  : {total_ht:,.2f} €")
        print(f"    → Total TTC : {total_ttc:,.2f} €")
        print(f"    → Payées    : {paid} / {len(customer_invoices)}")

    if supplier_invoices:
        total_ht = sum(
            float(inv.get("amount_eur_excl_taxes") or 0)
            for inv in supplier_invoices
        )
        total_ttc = sum(
            float(inv.get("amount_eur") or 0)
            for inv in supplier_invoices
        )
        paid = sum(1 for inv in supplier_invoices if inv.get("is_paid"))
        print(f"\n  Factures fournisseurs : {len(supplier_invoices)}")
        print(f"    → Total HT  : {total_ht:,.2f} €")
        print(f"    → Total TTC : {total_ttc:,.2f} €")
        print(f"    → Payées    : {paid} / {len(supplier_invoices)}")

    print(f"\n  Fichiers générés dans : {os.path.abspath(OUTPUT_DIR)}/")
    print("=" * 60)


# ─── Main ──────────────────────────────────────────────────────────────

def main():
    if not PENNYLANE_API_TOKEN:
        print("❌ Aucun token API configuré.")
        print("   Éditez config.py et renseignez PENNYLANE_API_TOKEN")
        sys.exit(1)

    ensure_output_dir()
    client = PennylaneClient()

    if not client.test_connection():
        sys.exit(1)

    customer_invoices = []
    supplier_invoices = []

    if EXTRACT_CUSTOMER_INVOICES:
        customer_invoices = extract_customer_invoices(client)
        transform_invoices_to_csv(
            customer_invoices,
            "Facture client",
            "odoo_factures_clients.csv",
        )

    if EXTRACT_SUPPLIER_INVOICES:
        supplier_invoices = extract_supplier_invoices(client)
        transform_invoices_to_csv(
            supplier_invoices,
            "Facture fournisseur",
            "odoo_factures_fournisseurs.csv",
        )

    print_summary(customer_invoices, supplier_invoices)
    print("\n✅ Extraction terminée !")
    print("   Prochaine étape : importer les CSV dans Odoo")


if __name__ == "__main__":
    main()
