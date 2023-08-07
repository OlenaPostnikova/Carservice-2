from odoo import fields, models

class AutoServiceMechanic(models.Model):
    _name = 'auto_service.mechanic'
    _description = 'Auto service mechanics'

    name = fields.Char(required=True,translate=True)
    active = fields.Boolean(
        default=True, )

    #jobs permitted
    job_ids = fields.One2many(comodel_name='auto_service.job_permitted', inverse_name='mechanic_id')

    #visit
    visit_ids = fields.One2many(comodel_name='auto_service.visit', inverse_name='mechanic_id')

    #timetable
    timetable_ids = fields.One2many(comodel_name='auto_service.timetable_mechanic',
                                    inverse_name='mechanic_id')
