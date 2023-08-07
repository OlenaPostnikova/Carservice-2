# -*- coding: utf-8 -*-
{
    'name': "MOT & service station",
    'summary': """ 
        MOT and all services for different type of vehicles
        """,
    'description': """
        Long description of module's purpose
    """,

    'author': "Olena Postnikova",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/security.xml',
        'security/ir.model.access.csv',

        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/auto_service_vehicle_views.xml',
        'views/auto_service_vehicle_manufacturer_views.xml',
        'views/auto_service_equipment_views.xml',
        'views/auto_service_mechanic_views.xml',
        'views/auto_service_job_views.xml',
        'views/auto_service_job_permitted_views.xml',
        'views/auto_service_visit.xml',
        'views/auto_service_timetable_mechanic_views.xml',
        'views/auto_service_timetable_equipment_views.xml',
        'wizard/new_timetable_wizard_view.xml',

        'views/auto_service_menus.xml',

        'data/auto_service_vehicle_manufacturer_demo.xml',
        'data/auto_service_res_partner_demo.xml',
        'data/auto_service_res_company_demo.xml',
        'data/auto_service_vehicle_demo.xml',
        'data/auto_service_equipment_demo.xml',
        'data/auto_service_mechanic_demo.xml',
        'data/auto_service_job_demo.xml',
        'data/auto_service_job_permitted_demo.xml',
        'data/auto_service_timetable_mechanic_demo.xml',
        'data/auto_service_timetable_equipment_demo.xml',

        'data/auto_service_visit_demo.xml',

        'reports/invoice_report.xml',
        'reports/invoice_reports_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
