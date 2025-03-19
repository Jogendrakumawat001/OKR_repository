# -*- coding: utf-8 -*-
# Copyright (C) Gilliam Management Services and Information Systems, Ltd. (the owner of Bizzup), 2021, 2022, 2023, 2024, 2025
# All Rights Reserved to Gilliam Management Services and Information Systems, Ltd.
# Unauthorized copying, editing or printing of this file, in any way is strictly prohibited
# Proprietary and confidential for more information, please contact
# lg@bizzup.app

from odoo import http
from odoo.http import request


class EventFeedbackController(http.Controller):
    """
    Controller for handling event feedback forms.
    """

    @http.route(
        ["/event-feedback/<int:event_id>"], type="http", auth="public", website=True
    )
    def event_feedback_form(self, event_id, **kwargs):
        """
        Renders the chef event feedback form with existing event data.
        """
        event = request.env["event.event"].sudo().browse(event_id)
        return request.render(
            "bizzup_event_customization.event_feedback_form", {"event": event}
        )

    @http.route(
        ["/shift-manager-event-feedback/<int:event_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def shift_manager_event_feedback_form(self, event_id, **kwargs):
        """
        Renders the employee event feedback form with existing event data.
        """
        event = request.env["event.event"].sudo().browse(event_id)
        return request.render(
            "bizzup_event_customization.shift_manager_event_feedback_form",
            {"event": event}
        )

    @http.route(
        "/event-feedback/submit_feedback",
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def event_submit_feedback(self, **post):
        """
        Handles form submission and updates the event record with feedback data.
        """
        event_id = int(post.get("event_id", 0))
        chef_id = post.get("chef_id")

        # Ensure chef_id is a valid integer before conversion
        if not chef_id or not chef_id.isdigit():
            return request.render(
                "bizzup_event_customization.event_feedback_form",
                {"event": request.env["event.event"].sudo().browse(event_id)}
            )

        chef_id = int(chef_id)
        event = request.env["event.event"].sudo().browse(event_id)

        chef_answers = request.env["chef.answer"].sudo().search(
            [('event_id', '=', event.id),('chef_id','=',chef_id)]
        )

        # Create feedback if no answers exist OR no answer exists for the chef
        if not chef_answers or not chef_answers:
            request.env["chef.answer"].sudo().create({
                "chef_id": chef_id,
                "event_id": event_id,
                "actual_participants": post.get("actual_participants", ""),
                "customer_satisfaction": post.get("customer_satisfaction",
                                                  ""),
                "unusual_problems": post.get("unusual_problems", ""),
                "is_chef_answer": True
            })

        return request.render(
            "bizzup_event_customization.event_feedback_thank_you"
        )

    @http.route(
        "/shift-manager-event-feedback/submit_feedback",
        type="http",
        auth="public",
        website=True,
        methods=["POST"],
    )
    def shift_manager_event_submit_feedback(self, **post):
        """
        Handles form submission and updates the event record with feedback data.
        """
        event_id = post.get("event_id")
        event = request.env["event.event"].sudo().browse(int(event_id))
        manager_id = event.shift_manager_id

        if not manager_id:
            return request.render(
                "bizzup_event_customization.shift_manager_event_feedback_form",
                {"event": request.env["event.event"].sudo().browse(event_id)}
            )

        chef_answers = request.env["chef.answer"].sudo().search([
            ("event_id", "=", event.id)
        ])

        if chef_answers:
            chef_answers.sudo().write({
                "shift_manager_id": manager_id.id,
                "is_shift_manager_answer": True
            })

        event.sudo().write({
            "notes_shift_manager": post.get("notes_shift_manager", ""),
        })

        return request.render(
            "bizzup_event_customization.event_feedback_thank_you"
        )
