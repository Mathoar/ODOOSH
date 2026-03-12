{
    "name": "Connecteur Pennylane",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "summary": "Import et suivi des factures fournisseurs depuis Pennylane",
    "description": """
        Module de connexion Pennylane pour FRAIS PEI / LPE.

        Fonctionnalités :
        - Import des factures fournisseurs via l'API Pennylane v2
        - Filtrage par période
        - Suivi du statut d'envoi (nouveau / envoyé / validé)
        - Classification des fournisseurs par entité, type et catégorie de charge
        - Historique des imports pour éviter les doublons
    """,
    "author": "FRAIS PEI",
    "website": "",
    "license": "LGPL-3",
    "depends": [
        "base",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/charge_category_data.xml",
        "views/res_partner_views.xml",
        "views/pennylane_invoice_views.xml",
        "views/pennylane_import_views.xml",
        "views/res_config_settings_views.xml",
        "views/menus.xml",
        "wizard/pennylane_import_wizard_views.xml",
    ],
    "external_dependencies": {
        "python": ["requests"],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
