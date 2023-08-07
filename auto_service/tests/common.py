from odoo.tests.common import TransactionCase


class TestCommon(TransactionCase):

    def setUp(self):
        super(TestCommon, self).setUp()
        self.group_auto_service_user = self.env.ref(
            'auto_service.group_auto_service_user')
        self.group_auto_service_admin = self.env.ref(
            'auto_service.group_auto_service_admin')
        self.auto_service_user = self.env['res.users'].create({
            'name': 'Auto Service User',
            'login': 'auto_service_user',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_auto_service_user.id)],
        })
        self.auto_service_admin = self.env['res.users'].create({
            'name': 'Auto Service Admin',
            'login': 'auto_service_admin',
            'groups_id': [(4, self.env.ref('base.group_user').id),
                          (4, self.group_auto_service_admin.id)],
        })

        # main objects
        self.vehicle_demo = self.env['auto_service.vehicle'].create({
            'name': 'Demo vehicle'})
        self.job_demo = self.env['auto_service.job'].create({
            'name': 'Demo job'})
        self.mechanic_demo = self.env['auto_service.mechanic'].create({
            'name': 'Demo mechanic'})
        self.equipment_demo = self.env['auto_service.equipment'].create({
            'name': 'Demo mechanic'})
        self.visit_demo = self.env['auto_service.visit'].create({
            'name': 'Demo visit'})

