{
    'name': 'FRAIS PEI - Base',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Module de base FRAIS PEI - Distribution surgelés La Réunion',
    'description': """
        Configuration de base pour FRAIS PEI (ex AH CHOU):
        - Champs personnalisés sur les partenaires (clients/fournisseurs)
        - Champs personnalisés sur les produits
        - Taxes TVA DOM (2.1% et 8.5%)
        - Listes de prix T1-T6
        - Conditions de paiement
    """,
    'author': 'FRAIS PEI',
    'website': '',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
        'purchase',
        'stock',
        'account',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/account_tax_data.xml',
        'data/product_pricelist_data.xml',
        'data/account_payment_term_data.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
