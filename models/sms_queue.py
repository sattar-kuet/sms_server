import random
import string

from odoo import fields, models


class SmsQueue(models.Model):
    _name = 'sms_server.queue'

    partner = fields.Many2one('res.partner')
    phone = fields.Char()
    message = fields.Text()
