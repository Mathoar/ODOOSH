"""
Test rapide de la connexion API Pennylane.
Usage : python test_connection.py
"""

import sys
from config import PENNYLANE_API_TOKEN
from pennylane_client import PennylaneClient


def main():
    if not PENNYLANE_API_TOKEN:
        print("❌ Aucun token API configuré.")
        print()
        print("Pour obtenir votre token Pennylane :")
        print("  1. Connectez-vous à Pennylane")
        print("  2. Allez dans : Paramètres > Connectivité > Développeurs")
        print("  3. Cliquez sur 'Générer un token API'")
        print("  4. Choisissez API V2, Lecture seule")
        print("  5. Copiez le token et collez-le dans config.py")
        print()
        print('  PENNYLANE_API_TOKEN = "votre_token_ici"')
        sys.exit(1)

    client = PennylaneClient()

    if client.test_connection():
        print("\n🎉 Tout est prêt ! Lancez l'extraction avec :")
        print("   python extract.py")
    else:
        print("\n💡 Vérifiez votre token dans config.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
