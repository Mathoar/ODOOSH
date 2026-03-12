{
    'name': 'FRAIS PEI - Import Données',
    'version': '19.0.1.0.0',
    'category': 'Tools',
    'summary': 'Import clients, fournisseurs, produits depuis Excel',
    'description': """
        Wizards d'import de données pour FRAIS PEI:
        - Import fournisseurs depuis Excel (feuille TRAME FRS)
        - Import clients depuis Excel (feuille trame client)
        - Import produits depuis Excel (feuille Trame articles)

        Transforme les scripts d'import AH CHOU en module Odoo natif.
    """,
    'author': 'FRAIS PEI',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'fraispei_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/import_wizard_views.xml',
    ],
    'external_dependencies': {
        'python': ['openpyxl'],
    },
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
