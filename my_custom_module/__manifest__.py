{
    'name': 'My Custom Module',
    'version': '19.0.1.0.0',
    'category': 'Uncategorized',
    'summary': 'Module personnalisé exemple pour Odoo.sh',
    'description': """
        Module d'exemple pour démarrer le développement sur Odoo.sh.
        Remplacez ce module par vos propres développements.
    """,
    'author': 'Mon Entreprise',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/my_model_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
