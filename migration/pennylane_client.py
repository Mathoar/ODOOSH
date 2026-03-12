"""
Client API Pennylane v2
Gère l'authentification, la pagination et les appels aux endpoints.
"""

import requests
import time
from config import PENNYLANE_API_TOKEN, PENNYLANE_API_BASE


class PennylaneClient:

    def __init__(self, token=None, base_url=None):
        self.token = token or PENNYLANE_API_TOKEN
        self.base_url = (base_url or PENNYLANE_API_BASE).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        })
        self._rate_limit_remaining = None

    def _request(self, method, path, params=None, max_retries=3):
        url = f"{self.base_url}{path}"
        for attempt in range(max_retries):
            resp = self.session.request(method, url, params=params)

            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", 5))
                print(f"  ⏳ Rate limit atteint, pause de {retry_after}s...")
                time.sleep(retry_after)
                continue

            if resp.status_code == 401:
                raise PermissionError(
                    "Token API invalide ou expiré. "
                    "Vérifiez PENNYLANE_API_TOKEN dans config.py"
                )

            resp.raise_for_status()
            return resp.json()

        raise RuntimeError(f"Échec après {max_retries} tentatives pour {url}")

    def _paginate(self, path, params=None):
        """Gère la pagination cursor-based de l'API v2."""
        params = dict(params or {})
        params.setdefault("per_page", 100)
        all_items = []
        page = 1

        while True:
            params["page"] = page
            data = self._request("GET", path, params=params)

            items = data.get("invoices") or data.get("invoice_lines") or data.get("data") or []
            if not items:
                break

            all_items.extend(items)
            total = data.get("total_items") or data.get("total") or 0
            print(f"  → {len(all_items)}/{total} enregistrements récupérés")

            if len(all_items) >= total or len(items) < params["per_page"]:
                break
            page += 1
            time.sleep(0.3)

        return all_items

    # ─── Factures clients ──────────────────────────────────────────────

    def list_customer_invoices(self, date_from=None, date_to=None):
        print("\n📋 Récupération des factures clients...")
        params = {}
        filters = []
        if date_from:
            filters.append({"field": "date", "operator": "gteq", "value": date_from})
        if date_to:
            filters.append({"field": "date", "operator": "lteq", "value": date_to})
        if filters:
            import json
            params["filter"] = json.dumps(filters)

        return self._paginate("/customer_invoices", params)

    def get_customer_invoice_lines(self, invoice_id):
        path = f"/customer_invoices/{invoice_id}/invoice_lines"
        data = self._request("GET", path)
        return data.get("invoice_lines") or data.get("data") or []

    # ─── Factures fournisseurs ─────────────────────────────────────────

    def list_supplier_invoices(self, date_from=None, date_to=None):
        print("\n📋 Récupération des factures fournisseurs...")
        params = {}
        filters = []
        if date_from:
            filters.append({"field": "date", "operator": "gteq", "value": date_from})
        if date_to:
            filters.append({"field": "date", "operator": "lteq", "value": date_to})
        if filters:
            import json
            params["filter"] = json.dumps(filters)

        return self._paginate("/supplier_invoices", params)

    def get_supplier_invoice_lines(self, invoice_id):
        path = f"/supplier_invoices/{invoice_id}/invoice_lines"
        data = self._request("GET", path)
        return data.get("invoice_lines") or data.get("data") or []

    # ─── Test de connexion ─────────────────────────────────────────────

    def test_connection(self):
        """Vérifie que le token fonctionne."""
        print("🔌 Test de connexion à l'API Pennylane...")
        try:
            data = self._request("GET", "/customer_invoices", params={"per_page": 1})
            total = data.get("total_items") or data.get("total") or "?"
            print(f"✅ Connexion réussie ! {total} facture(s) client trouvée(s)")
            return True
        except PermissionError as e:
            print(f"❌ {e}")
            return False
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")
            return False
