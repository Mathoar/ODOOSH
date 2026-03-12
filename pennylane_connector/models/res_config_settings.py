from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pennylane_api_token = fields.Char(
        string="Token API Pennylane",
        config_parameter="pennylane_connector.api_token",
    )
    pennylane_api_base_url = fields.Char(
        string="URL de base API",
        config_parameter="pennylane_connector.api_base_url",
        default="https://app.pennylane.com/api/external/v2",
    )
