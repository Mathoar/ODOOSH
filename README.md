# FRAIS PEI - Odoo.sh 19.0

Modules personnalisés Odoo pour **FRAIS PEI** (ex AH CHOU SARL) - Distribution de surgelés, La Réunion.

## Modules

### fraispei_base

Module de base contenant :
- **Champs personnalisés partenaires** : groupes clients (GBH, SMDIS, Cellule U...), enseignes (Carrefour, Leclerc, Run Market...), groupes fournisseurs (Asie/Inde, Europe, Local...), blocage, taux RFA, etc.
- **Champs personnalisés produits** : conditionnement, PCB, zone de pêche, nom scientifique, marque, origine, grille tarifaire T1-T6, coefficient d'approche, taux octroi de mer
- **Données de configuration** : Taxes TVA DOM (2.1% et 8.5%), Listes de prix (Base + T1 à T6), Conditions de paiement (15j, 30j, 60j)

### fraispei_import

Wizard d'import de données depuis Excel :
- **Fournisseurs** : depuis la feuille "TRAME FRS"
- **Clients** : depuis la feuille "trame client"
- **Produits** : depuis la feuille "Trame articles"

Accessible via le menu **FRAIS PEI > Import Données** dans Odoo.
Supporte le mode simulation (dry-run) et la limite d'import.

## Démarrage rapide

1. Connectez-vous sur [odoo.sh](https://www.odoo.sh)
2. Liez ce dépôt GitHub au projet
3. Sélectionnez **Odoo 19.0**
4. Installez `fraispei_base` puis `fraispei_import`
5. Importez vos données via **FRAIS PEI > Import Données**

## Structure

```
├── fraispei_base/
│   ├── __manifest__.py
│   ├── models/
│   │   ├── res_partner.py          # Champs clients/fournisseurs
│   │   └── product_template.py     # Champs produits
│   ├── views/
│   │   ├── res_partner_views.xml   # Onglet FRAIS PEI sur les fiches
│   │   └── product_template_views.xml
│   └── data/
│       ├── account_tax_data.xml    # TVA 2.1% et 8.5% DOM
│       ├── product_pricelist_data.xml  # Tarifs T1-T6
│       └── account_payment_term_data.xml
│
├── fraispei_import/
│   ├── __manifest__.py
│   ├── wizards/
│   │   └── import_wizard.py        # Wizard d'import Excel
│   ├── views/
│   │   └── import_wizard_views.xml
│   └── security/
│       └── ir.model.access.csv
│
├── requirements.txt                # openpyxl
└── README.md
```
