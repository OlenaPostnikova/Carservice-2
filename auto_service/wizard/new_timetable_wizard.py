from odoo import models, fields
from datetime import timedelta,datetime

class TimetableLineWizard(models.TransientModel):
    # часы работы механика
    _name = 'timetable.line.wizard'
    _description = 'New timetable lines'

    mechanic_id = fields.Many2one(comodel_name='auto_service.mechanic')
    date = fields.Date('Date')
    # для расчетов
    start_time_int = fields.Integer(string='From')
    end_time_int = fields.Integer(string='To')
    # для хранения в расписании
    # start_time = fields.Datetime(string='From')
    # end_time = fields.Datetime(string='To')
class NewTimetableWizard(models.TransientModel):
    _name = 'new.timetable.wizard'
    _description = 'Create new mechanic timetable'

    mechanic_id = fields.Many2one(comodel_name='auto_service.mechanic',
                                string='Mechanic',
                                required=True)
    # задаваемые параметры - период и часы работы
    start_date = fields.Date('Start date')
    end_date = fields.Date('End date')
    start_time_int = fields.Integer(string='From')
    end_time_int = fields.Integer(string='to')
    # строки расписания (day + time)
    timetable_line_ids = fields.Many2many('timetable.line.wizard')
    #print(current_date.strftime("%d-%m-%y %H:%M"))
    # date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

    def _compute_one_date_line(self, current_date):
        for rec in self:
            # start_time = current_date+timedelta(hours=self.start_time_int)
            # end_time = current_date + timedelta(hours=self.end_time_int)

            date_time_str = str(current_date) + ' '+ str(self.start_time_int) + ':00:00'
            print(date_time_str)
            start_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

            date_time_str = str(current_date) + ' '+ str(self.end_time_int) + ':00:00'
            end_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

            new_line = {
                'date': current_date,
                'mechanic_id': rec.mechanic_id.id,
                'start_time_int': self.start_time_int,
                'end_time_int': self.end_time_int,
                'start_time': start_time,
                'end_time': end_time,
            }
            # пишем в табличку на экране
            # rec.timetable_line_ids.create(new_line)
            # + в расписание
            self.env['auto_service.timetable_mechanic'].create(new_line)
    def action_create(self):

        # расчет строк визарда timetable_line_ids
        current_date = self.start_date
        while current_date <= self.end_date:
            print(current_date)
            self._compute_one_date_line(current_date)
            current_date = current_date + timedelta(days=1)

        # # запись из строк визарда timetable_line_ids в модель timetable_mechanic
        # for rec in self:
        #     for line in self.timetable_line_ids:
        #         print('****************************=' + str(line.date))
        #         self.env['auto_service.timetable_mechanic'].create({
        #             'mechanic_id': rec.mechanic_id.id,
        #             'date': line.date,
        #             'start_time': line.start_time_int,
        #             'end_time': line.end_time_int,
        #         })
