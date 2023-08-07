from odoo import models, fields, api
# from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class AutoServiceVehicle(models.Model):
    _name = 'auto_service.vehicle'
    _description = 'Auto service vehicles'

    name = fields.Char(required=True)
    active = fields.Boolean(
        default=True, )

    vehicle_make_id = fields.Many2one(comodel_name='auto_service.vehicle_manufacturer', string='Vehicle make')
    model = fields.Char(required=False, string='Model')
    VIN = fields.Char(required=False, string='VIN')
    registration_number = fields.Char(required=False, string='Registration')
    year_manufacture = fields.Date('Year of manufacture')
    car_mileage = fields.Integer(required=False, string='Car mileage')
    date_next_MOT = fields.Date('Date of next MOT')

    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')

    #visit history
    visit_ids = fields.One2many(comodel_name='auto_service.visit',
                                inverse_name='vehicle_id')
    @api.depends('vehicle_make_id', 'model', 'registration_number')
    def _compute_name(self):
        """Determine field name to display in the
                 Changes on the fields
                 :param 'vehicle_make_id', 'model', 'registration_number'
                 :return None:
                 """
        for rec in self:
            print(rec.vehicle_make_id.name)
            rec.name = '%s %s %s' % \
                       (rec.vehicle_make_id.name, rec.model, rec.registration_number)

