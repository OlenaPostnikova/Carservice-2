# from odoo.addons.auto_service.tests.common import TestCommon
from .common import TestCommon
from odoo.fields import Command
from odoo.tests import tagged
from odoo.exceptions import UserError
from odoo.exceptions import AccessError
from datetime import timedelta, datetime

@tagged('post_install', '-at_install')
class TestJob(TestCommon):

    def test_job_creation(self):

        self.equipment = self.env['auto_service.equipment'].create({'name': 'Office Chair'})

        test_template = self.env['auto_service.job'].create({
            'name': 'New job',
            'duration': 2,
            'equipment_id' : self.equipment.id
        })

@tagged('post_install', '-at_install')
class TestJobPermitted(TestCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.job = cls.env['auto_service.job'].create({'name': 'New job'})
        cls.mechanic = cls.env['auto_service.mechanic'].create({'name': 'New mechanic'})

        cls.job_permitted = cls.env['auto_service.job_permitted'].create({
            'job_id': cls.job,
            'mechanic_id': cls.mechanic,
        })

@tagged('post_install', '-at_install')
class TestVisit(TestCommon):

    @classmethod
    def setUpClass(cls):
        """Check all key control procedures
                  1) _check_mechanic_timetable (mechanic has working hours at the new date according timetable)
                  2) _check_mechanic_is_busy (there is no other visit with this mechanic at the same time)
                  3) _check_equipment_timetable (there is no planned maintenance for this equipment according timetable)
                  4) _check_equipment_is_busy (there is no other visit with this equipment at the same time)
                  5) _check_vehicle_is_busy (there is no other visit with this vehicle at the same time)
                """

        super().setUpClass()

        cls.Alex_id = cls.env['auto_service.mechanic'].create({'name': 'Alex'}).id
        cls.Fisher_id = cls.env['auto_service.mechanic'].create({'name': 'Fisher',}).id
        cls.Tom_id = cls.env['auto_service.mechanic'].create({'name': 'Tompson', }).id

        cls.timetableAlex = cls.env['auto_service.timetable_mechanic'].create({
            'name': 'Alex',
            'mechanic_id': cls.Alex_id,
            'date': datetime.now(),
            'start_time_int': 9,
            'end_time_int': 18,
        })

        cls.stand1_id = cls.env['auto_service.equipment'].create({'name': 'stand',}).id
        cls.wheel_adjustment_id = cls.env['auto_service.job'].create({
                        'name': 'wheel adjustment',
                        'equipment_id': cls.stand1_id,
                        'duration':2,
                        'price': 30,
                        }).id

        cls.volvo7596_id = cls.env['auto_service.vehicle'].create({'name': 'volvo AA7596',}).id
        cls.fordZY1ABC_id = cls.env['auto_service.vehicle'].create({'name': 'ford ZY1 ABC',}).id

        cls.visit1 = cls.env['auto_service.visit'].create({
            'visit_date': datetime.now(),
            'start_time_int': 10,
            'end_time_int': 12,
            'duration': 2,
            'mechanic_id': cls.Alex_id,
            'vehicle_id': cls.volvo7596_id,
            'job_id': cls.wheel_adjustment_id,
            'equipment_id': cls.stand1_id,
        }),

    def test_action_compute_time(self):
        self.visit_demo.write({'visit_date': datetime.now(), 'start_time_int': 10, 'end_time_int': 2})
        self.visit_demo.with_user(self.auto_service_admin)._compute_time()

          # I check sale price of Laptop.
          #   product = self.laptop_E5023
          #   price = self.customer_pricelist._get_product_price(product, quantity=1.0)
          #   msg = "Wrong sale price: Laptop. should be %s instead of %s" % (price, (product.lst_price + 1))
          #   self.assertEqual(float_compare(price, product.lst_price + 1, precision_digits=2), 0, msg)

