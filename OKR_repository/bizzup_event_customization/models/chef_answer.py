from odoo import models, fields


class ChefAnswer(models.Model):
    _name = "chef.answer"
    _description = "Chef Answers"
    _rec_name = 'chef_id'

    chef_id = fields.Many2one("hr.employee", string="Chef", required=True)
    actual_participants = fields.Char(string="Actual Participants")
    customer_satisfaction = fields.Text(string="Customer Satisfaction")
    unusual_problems = fields.Text(string="Unusual Problems")
    
    event_id = fields.Many2one('event.event')
    is_chef_answer = fields.Boolean("Chef answer", readonly=True,
                                    copy=False,)
    is_shift_manager_answer = fields.Boolean("Shift Manager answer",
                                             readonly=True,
                                             copy=False, )
    shift_manager_id = fields.Many2one("hr.employee",string="Shift Manager")
    address_id = fields.Many2one(related="event_id.address_id")
    user_id = fields.Many2one(related="event_id.user_id")
    date_begin = fields.Datetime(related="event_id.date_begin")
    date_end = fields.Datetime(related="event_id.date_end")
