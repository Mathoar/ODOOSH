"""
Configuration pour la migration Pennylane → Odoo
FRAIS PEI - La Réunion
"""

# ─── Token API Pennylane ───────────────────────────────────────────────
# Générez votre token dans Pennylane :
# Paramètres > Connectivité > Développeurs > Générer un token API
# Choisissez : API V2, Lecture seule, puis copiez le token ci-dessous.
PENNYLANE_API_TOKEN = ""

# ─── URL de base API Pennylane ─────────────────────────────────────────
PENNYLANE_API_BASE = "https://app.pennylane.com/api/external/v2"

# ─── Options d'extraction ──────────────────────────────────────────────
# Filtrer par date (format YYYY-MM-DD), laisser vide pour tout récupérer
DATE_FROM = ""
DATE_TO = ""

# Types de factures à extraire
EXTRACT_CUSTOMER_INVOICES = True
EXTRACT_SUPPLIER_INVOICES = True

# Télécharger les PDF des factures
DOWNLOAD_DOCUMENTS = False

# ─── Dossier de sortie ─────────────────────────────────────────────────
OUTPUT_DIR = "output"
