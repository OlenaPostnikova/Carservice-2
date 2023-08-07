# -*- coding: utf-8 -*-
# from odoo import http


# class /home/admin16/opt/odoo-16.0/repositories/olenapostnikova/autoService(http.Controller):
#     @http.route('//home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service//home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service//home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service.listing', {
#             'root': '//home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service//home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service',
#             'objects': http.request.env['/home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service./home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service'].search([]),
#         })

#     @http.route('//home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service//home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service/objects/<model("/home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service./home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/home/admin16/opt/odoo-16.0/repositories/olenapostnikova/auto_service.object', {
#             'object': obj
#         })
