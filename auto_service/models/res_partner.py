from odoo import models, fields


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    is_auto_service_customer = fields.Boolean('Is autoservice customer')
    customer_details = fields.Char(required=False, string='Customer details')