import random
import string

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_sms_token(self):
        length = 12
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    sms_token = fields.Char(string='SMS Token', default=_default_sms_token)
