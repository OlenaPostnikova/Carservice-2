# module event_sale - не вийшло додати наслiдування як у них
# from odoo import api, fields, models
# class Product(models.Model):
#     _inherit = 'product.product'
#
#     event_ticket_ids = fields.One2many('event.event.ticket', 'product_id', string='Event Tickets')

from odoo import fields, models

class AutoServiceJob(models.Model):
    _name = 'auto_service.job'
    _description = 'Auto service jobs and required equipment'
#    _inherit = 'product.product'

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(
        default=True, )

    equipment_id = fields.Many2one(comodel_name='auto_service.equipment', string='Required equipment')
    duration = fields.Integer(required=False, default=1, string='Duration,hours')
    price = fields.Float(required=False, string='Price,£')
    comment = fields.Char(string='Comment', translate=True)

    mechanic_ids = fields.One2many(comodel_name='auto_service.job_permitted', inverse_name='mechanic_id')
