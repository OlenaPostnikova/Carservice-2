from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import timedelta,datetime

class AutoServiceVisit(models.Model):
    _name = 'auto_service.visit'
    _description = "Car service visit"

    name = fields.Char(translate=True)
    active = fields.Boolean(
        default=True, )

    visit_date = fields.Date('Date', readonly=False,
                             states={'visit has been done': [('readonly', True)]})
    # for calculations
    start_time_int = fields.Integer(string='Hours from')
    end_time_int = fields.Integer(string='Hours to')
    # for timetable store
    start_time = fields.Datetime(string='From')
    end_time = fields.Datetime(string='to')

    vehicle_id = fields.Many2one('auto_service.vehicle', string='Vehicle')
    customer_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    problem = fields.Char(string='Description of the problem(s)',translate=True)
    car_mileage = fields.Integer(required=False, string='Car mileage')

    equipment_id = fields.Many2one('auto_service.equipment', string='Equipment required')
    mechanic_id = fields.Many2one('auto_service.mechanic', string='Mechanic')

    job_id = fields.Many2one('auto_service.job', string='Job')
    job_recommended_id = fields.Many2one('auto_service.job', string='Job recommended')
    duration = fields.Integer(required=False, default=1, string='Duration,hours')
    price = fields.Float(required=False, string='Price,£')

    is_done = fields.Boolean()
    recommendation = fields.Text(string='Recommendation',translate=True)
    comment = fields.Char(string='Comment',translate=True)

    state = fields.Char(compute='_compute_state')
    # state_not_delete = fields.Char(compute='_compute_state_not_delete')
    state_not_delete = fields.Char(compute='_compute_state')

    @api.onchange('vehicle_id')
    def _compute_mileage_customer(self):
        """Determine fields car_mileage,customer_id after entering the value of vehicle_id
              :param None:
              :return None:
              """
        for rec in self:
            if rec.vehicle_id:
                rec.car_mileage = rec.vehicle_id.car_mileage
                rec.customer_id = rec.vehicle_id.customer_id

    @api.onchange('job_id')
    def _compute_equipment_onchange(self):
        """Determine fields equipment_id,duration,price after entering the value of job_id
            :param None:
            :return None:
            """
        for rec in self:
            if rec.job_id:
                rec.equipment_id = rec.job_id.equipment_id.id
                rec.duration = rec.job_id.duration
                rec.price = rec.job_id.price

    @api.ondelete(at_uninstall=False)
    def _unlink_only_if_open(self):
        """Prohibit delete visit if visit have been done
            :param None:
            :return None:
            """
        for statement in self:
            if statement.is_done:
                raise UserError(
                    'Not allowed to delete appointment'
                    'Visit has been done')

    @api.depends('is_done')
    def _compute_state(self):
        """Change service fields state and state_not_delete after change value is_done
            :param None:
            :return None:
            """
        for rec in self:
            if rec.is_done:
                rec.state = 'visit has been done'
                rec.state_not_delete = True
            else:
                rec.state = 'visit has not been done'
                rec.state_not_delete = False

    @api.onchange('visit_date', 'start_time_int', 'duration')
    def _check_visit_date_(self):
        """Controls whether the date can be changed
            Required conditions:
                1) mechanic has working hours at the new date according timetable
                2) there is no other visit with this mechanic at the same time
                3) there is no other visit with this equipment at the same time
                4) there is no other visit with this equipment at the same time
              :param None:
              :return None:
              """
        if self.visit_date:
            self._compute_time()
            self._check_mechanic_timetable()
            self._check_equipment_timetable()
            self._check_mechanic_is_busy()
            self._check_equipment_is_busy()
            self._check_vehicle_is_busy()

    @api.onchange('mechanic_id')
    def _check_mechanic_(self):
        self._check_mechanic_timetable()
        self._check_mechanic_is_busy()

    @api.onchange('job_id', 'equipment_id')
    def _check_equipment_(self):
        self._check_equipment_timetable()
        self._check_equipment_is_busy()

    @api.constrains('visit_date', 'mechanic_id', 'equipment_id', 'vehicle_id')
    def check_visit(self):
        """Controls whether the date can be changed
              Required conditions:
                  1) mechanic has working hours at the new date according timetable
                  2) there is no other visit with this mechanic at the same time
                  3) there is no planned maintenance for this equipment according timetable
                  4) there is no other visit with this equipment at the same time
                  5) there is no other visit with this vehicle at the same time
                :param None:
                :return None:
                """
        if self.mechanic_id:
            self._check_mechanic_timetable()
            self._check_mechanic_is_busy()

        if self.equipment_id:
            self._check_equipment_timetable()
            self._check_equipment_is_busy()

        if self.vehicle_id:
            self._check_vehicle_is_busy()

    def _time_conversion(self, date, time_int):
        """Convert date as date to datetime (date + quantity of hours)
                :param date: date as date
                :param time_int: quantity of hours
                :return date: as datetime
                """
        if time_int <= 9:
            date_time_str = str(date) + ' 0' + str (time_int) + ':00:00'
        else:
            date_time_str = str(date) + ' ' + str (time_int) + ':00:00'

        return datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    def _compute_time(self):
        """Compute end time after entering visit_date, start time or duration
            :param None:
            :return None:
            """
        for rec in self:
            if rec.visit_date and rec.start_time_int and rec.duration:
                rec.end_time_int = rec.start_time_int + rec.duration
                # Convert hours integer to date
                rec.start_time = self._time_conversion(rec.visit_date, rec.start_time_int)
                rec.end_time = self._time_conversion(rec.visit_date, rec.end_time_int)

    def _if_time_slots_cross(self, start1, end1, start2, end2):
        """Determine do the slots overlap
              :param start1,end1 - start and end of the first time interval (e.g. visit period)
                     start2,end2 - start and end of the first time interval (e.g. maintenance timetable or other visit)
              :return True: if time slots are intersected
                      False: if not
              """
        if (start1 >= start2 and start1 <= end2) or (end1 >= start2 and end1 <= end2):
            # if the start date or end date of the interval being checked falls into the middle of another,
            # then they intersect
            return True
        else:
            return False

    def _if_time_slot_in_another(self, start1, end1, start2, end2):
        """Determine if the time interval is included in another
             :param start1,end1 - the first slot in which we are looking for (e.g. timetable)
                    start2,end2 - the second slot is looking for inside the first one (e.g. visit period)
             :return True: if first slot is including second
                     False: if not
             """
        if (start1 <= start2 and end1 >= end2):
            # if the first interval is wider than the second
            return True
        else:
            return False

    def _check_mechanic_timetable(self):
        """Check whether mechanic has working hours at the new date according timetable
               :param None:
               :return True/False: True if mechanic has working hours at the date & time of visit
                                   False if not
               """

        for rec in self:

            if not rec.mechanic_id or not rec.visit_date:
                return True

            #select of all schedule entries of the selected mechanic for the selected date
            result_search = rec.mechanic_id.timetable_ids.search([
                ('mechanic_id', '=', rec.mechanic_id.id),
                ('date', '=', rec.visit_date)
            ])
            for rec_search_time_table in result_search:
                # select all timetable records for this date and compare 2 time slots :
                #   - working hours according timetable (rec_search_time_table)
                #   - current visit period, calculated as visit start_time + job duration (rec)
                if self._if_time_slot_in_another(
                        rec_search_time_table.start_time_int,
                        rec_search_time_table.end_time_int,
                        rec.start_time_int,
                        rec.start_time_int + rec.duration
                ):
                    #the time interval of the visit is not included in the time slot according to the schedule
                    return False
                else:
                    # the time interval of the visit is included in the time slot according to the schedule
                    return True
            # time slot for chosen date in timetable was not found
            raise (UserError('' + rec.mechanic_id.name + ' : no timesheet at that time'))
            return False

    def _check_equipment_timetable(self):
        """Determine if the equipment repair is planned for this time
            On the contrary look for there to be no record
                :param None:
                :return True/False: True if time slot equipment maintenance intersects visit period
                                    False if not
                """
        for rec in self:

            if not (rec.equipment_id or rec.visit_date):
                return True

            result_search = rec.equipment_id.timetable_ids.search([
                ('equipment_id', '=', rec.equipment_id.id),
                ('date', '=', rec.visit_date)
            ])
            for rec_search_time_table in result_search:
                # select all maintenance timetable records for this date and compare 2 time slots :
                #   - current visit period, calculated as visit start_time + job duration (rec)
                #   - maintenance hours according equipment maintenance timetable (rec_search_time_table)
                if self._if_time_slots_cross(rec.start_time_int,
                                             rec.start_time_int + rec.duration,
                                             rec_search_time_table.start_time_int,
                                             rec_search_time_table.end_time_int):
                    # maintenance hours and visit time intersect
                    raise (UserError('' + rec.equipment_id.name + ' : no timesheet at that time'))
                    return False
            # there is no maintenance hours intersected with this visit time
            return True

    def _check_mechanic_is_busy(self):
        """Check whether mechanic has other visit this date & time slot
                  :param None:
                  :return True/False: True if mechanic has other visit at the date & time of visit
                                      False if not
                  """
        for rec in self:

            if not rec.mechanic_id or not rec.visit_date or not rec.id:
                return True

            result_search = self.search([
                ('mechanic_id', '=', rec.mechanic_id.id),
                ('visit_date', '=', rec.visit_date),
                ('id', '!=', rec.id)
            ])
            # select all other visit records on this date & mechanic and compare 2 time slots :
            #   - current visit period, calculated as visit start_time + job duration (rec)
            #   - other visit period (rec_search_other_visit)
            for rec_search_other_visit in result_search:

                if self._if_time_slots_cross(rec.start_time_int,
                                             rec.start_time_int + rec.duration,
                                             rec_search_other_visit.start_time_int,
                                             rec_search_other_visit.end_time_int):
                    raise (UserError('' + rec.mechanic_id.name + ' : other visit at that time'))
                    return False

            return True

    def _check_equipment_is_busy(self):
        """Check whether equipment has other visit this date & time slot
                    :param None:
                    :return True/False: True if equipment has other visit at the date & time of visit
                                        False if not
                    """
        pass
        for rec in self:

            if not rec.equipment_id or not rec.visit_date or not rec.id:
                return True

            result_search = self.search([
                ('vehicle_id', '=', rec.equipment_id.id),
                ('visit_date', '=', rec.visit_date),
                ('id', '!=', rec.id)
            ])
            # select all other visit records on this date & equipment and compare 2 time slots :
            #   - current visit period, calculated as visit start_time + job duration (rec)
            #   - other visit period (rec_search_other_visit)
            for rec_search_other_visit in result_search:
                if self._if_time_slots_cross(rec.start_time_int,
                                             rec.start_time_int + rec.duration,
                                             rec_search_other_visit.start_time_int,
                                             rec_search_other_visit.end_time_int):
                    raise (UserError('' + rec.equipment_id.name + ' : other visit at that time'))

    def _check_vehicle_is_busy(self):
        """Check whether vehicle has other visit this date & time slot
             :param None:
             :return True/False: True if vehicle has other visit at the date & time of visit
                                 False if not
             """
        for rec in self:

            if not rec.vehicle_id or not rec.visit_date or not rec.id:
                return True

            result_search = self.search([
                ('vehicle_id', '=', rec.vehicle_id.id),
                ('visit_date', '=', rec.visit_date),
                ('id', '!=', rec.id)
            ])
            # select all other visit records on this date & equipment and compare 2 time slots :
            #   - current visit period, calculated as visit start_time + job duration (rec)
            #   - other visit period (rec_search_other_visit)
            for rec_search_other_visit in result_search:
                if self._if_time_slots_cross(rec.start_time_int,
                                             rec.start_time_int + rec.duration,
                                             rec_search_other_visit.start_time_int,
                                             rec_search_other_visit.end_time_int):
                    raise (UserError('' + rec.vehicle_id.name + ' : other visit at that time'))


