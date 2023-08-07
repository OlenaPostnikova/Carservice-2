from odoo import fields, models

# работы, разрешенные механику
class AutoServiceJobPermited(models.Model):
    _name = 'auto_service.job_permitted'
    _description = 'Auto service woks permitted for mechanic'

    job_id = fields.Many2one('auto_service.job')
    mechanic_id = fields.Many2one('auto_service.mechanic')

