# -*- coding: utf-8 -*-
# Copyright (C) Gilliam Management Services and Information Systems, Ltd. (the owner of Bizzup), 2021, 2022, 2023, 2024, 2025
# All Rights Reserved to Gilliam Management Services and Information Systems, Ltd.
# Unauthorized copying, editing or printing of this file, in any way is strictly prohibited
# Proprietary and confidential for more information, please contact
# lg@bizzup.app


from odoo import models, fields


class EventEvent(models.Model):
    """
    Extends `event.event` model to add fields for event management.
    """

    _inherit = "event.event"

    chef_ids = fields.Many2many("hr.employee", string="Chefs")
    employee_in_charge_id = fields.Many2one("hr.employee", string="Employee in Charge")
    customer_id = fields.Many2one("res.partner", string="Customer")
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
    base_url = fields.Char(
        default=lambda self: self.env["ir.config_parameter"]
        .sudo()
        .get_param("web.base.url")
    )
    shift_manager_id = fields.Many2one("hr.employee",string="Shift Manager")

    # Left Group (Event Review & Notes)
    actual_participants = fields.Char(string="Actual Participants")
    customer_satisfaction = fields.Text(string="Customer Satisfaction")
    unusual_problems = fields.Text(string="Unusual Problems")
    notes_shift_manager = fields.Text(string="Notes of Shift Managers")
    financial_notes = fields.Text(string="Financial Notes")

    chef_answer_ids = fields.One2many('chef.answer', 'event_id',
                                      'Chef Answer')


    # Right Group (Event Requirements & Details)
    sensitivities = fields.Char(string="Sensitivities")
    vegans_number = fields.Integer(string="Vegans Number")
    vegetarians_number = fields.Integer(string="Vegetarians Number")
    wines = fields.Selection([("YES", "YES"), ("NO", "NO")], string="Wines")
    beer = fields.Selection([("YES", "YES"), ("NO", "NO")], string="Beer")
    soft_drink = fields.Selection([("YES", "YES"), ("NO", "NO")],
                                  string="Soft Drink")
    apron_number = fields.Integer(string="Apron Number")
    notes_for_chef = fields.Text(string="Notes for the Chef")

