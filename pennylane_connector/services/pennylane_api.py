"""
Client API Pennylane v2 pour Odoo.
Gère l'authentification, la pagination et les appels aux endpoints.
"""

import json
import logging
import time

import requests

_logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://app.pennylane.com/api/external/v2"
PER_PAGE = 100
RATE_LIMIT_PAUSE = 5
REQUEST_DELAY = 0.3
MAX_RETRIES = 3


class PennylaneAPI:

    def __init__(self, token, base_url=None):
        self.token = token
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        })

    def _request(self, method, path, params=None):
        url = f"{self.base_url}{path}"
        for attempt in range(MAX_RETRIES):
            try:
                resp = self.session.request(method, url, params=params, timeout=30)
            except requests.exceptions.RequestException as e:
                _logger.warning("Pennylane API request error (attempt %d): %s", attempt + 1, e)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RATE_LIMIT_PAUSE)
                    continue
                raise

            if resp.status_code == 429:
                retry_after = int(resp.headers.get("Retry-After", RATE_LIMIT_PAUSE))
                _logger.info("Rate limited, waiting %ds", retry_after)
                time.sleep(retry_after)
                continue

            if resp.status_code == 401:
                raise PermissionError("Token API Pennylane invalide ou expiré.")

            resp.raise_for_status()
            return resp.json()

        raise RuntimeError(f"Échec après {MAX_RETRIES} tentatives pour {url}")

    def _paginate(self, path, params=None):
        params = dict(params or {})
        params.setdefault("per_page", PER_PAGE)
        all_items = []
        page = 1

        while True:
            params["page"] = page
            data = self._request("GET", path, params=params)

            items = (
                data.get("invoices")
                or data.get("invoice_lines")
                or data.get("data")
                or []
            )
            if not items:
                break

            all_items.extend(items)
            total = data.get("total_items") or data.get("total") or 0
            _logger.info("Pennylane: fetched %d/%d records from %s", len(all_items), total, path)

            if len(all_items) >= total or len(items) < PER_PAGE:
                break

            page += 1
            time.sleep(REQUEST_DELAY)

        return all_items

    # ─── Public methods ────────────────────────────────────────────────

    def test_connection(self):
        try:
            data = self._request("GET", "/customer_invoices", params={"per_page": 1})
            total = data.get("total_items") or data.get("total") or 0
            return True, f"Connexion OK – {total} facture(s) client trouvée(s)"
        except PermissionError:
            return False, "Token API invalide ou expiré"
        except Exception as e:
            return False, f"Erreur de connexion : {e}"

    def fetch_supplier_invoices(self, date_from=None, date_to=None):
        params = {}
        filters = []
        if date_from:
            filters.append({"field": "date", "operator": "gteq", "value": str(date_from)})
        if date_to:
            filters.append({"field": "date", "operator": "lteq", "value": str(date_to)})
        if filters:
            params["filter"] = json.dumps(filters)

        return self._paginate("/supplier_invoices", params)

    def fetch_customer_invoices(self, date_from=None, date_to=None):
        params = {}
        filters = []
        if date_from:
            filters.append({"field": "date", "operator": "gteq", "value": str(date_from)})
        if date_to:
            filters.append({"field": "date", "operator": "lteq", "value": str(date_to)})
        if filters:
            params["filter"] = json.dumps(filters)

        return self._paginate("/customer_invoices", params)

    def fetch_invoice_lines(self, invoice_id, invoice_type="supplier"):
        prefix = "supplier_invoices" if invoice_type == "supplier" else "customer_invoices"
        path = f"/{prefix}/{invoice_id}/invoice_lines"
        try:
            data = self._request("GET", path)
            return data.get("invoice_lines") or data.get("data") or []
        except Exception as e:
            _logger.warning("Cannot fetch lines for invoice %s: %s", invoice_id, e)
            return []
