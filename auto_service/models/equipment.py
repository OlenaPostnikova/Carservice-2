from odoo import models, fields

class AutoServiceEquipment(models.Model):
    _name = 'auto_service.equipment'
    _description = 'Auto service equipment'

    name = fields.Char(required=True,translate=True)
    active = fields.Boolean(
        default=True, )

    # visit
    visit_ids = fields.One2many(comodel_name='auto_service.visit', inverse_name='mechanic_id')

    #timetable
    timetable_ids = fields.One2many(comodel_name='auto_service.timetable_equipment',
                                              inverse_name='equipment_id')
