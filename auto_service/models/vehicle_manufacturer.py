from odoo import models, fields

class AutoServiceVehicleManufacturer(models.Model):
    _name = 'auto_service.vehicle_manufacturer'
    _description = 'Auto service vehicle manufacturers'

    name = fields.Char(required=True,translate=True)
    active = fields.Boolean(
        default=True, )
