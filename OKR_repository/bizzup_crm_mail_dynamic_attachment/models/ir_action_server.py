# -*- coding: utf-8 -*-
# Copyright (C) Gilliam Management Services and Information Systems, Ltd. (the owner of Bizzup), 2021, 2022, 2023, 2024, 2025
# All Rights Reserved to Gilliam Management Services and Information Systems, Ltd.
# Unauthorized copying, editing, or printing of this file, in any way, is strictly prohibited.
# Proprietary and confidential. For more information, please contact lg@bizzup.app

from odoo import models


class ServerAction(models.Model):
    """
    Inherits 'ir.actions.server' to modify email automation behavior.
    """

    _inherit = "ir.actions.server"

    def _run_action_mail_post_multi(self, eval_context=None):
        """
        Overrides the default mail posting action to dynamically attach
        country-specific PDFs.

        - Identifies if the action is triggered for CRM leads when the stage changes to 'Schedule Meeting'.
        - Removes old attachments from the email template.
        - Searches for relevant PDFs based on the lead's country fields.
        - Attaches the corresponding PDFs to the email template before sending.

        :param eval_context: Context dictionary for evaluating server actions.
        :return: Calls the parent method to proceed with the email sending process.
        """
        automation_records = self._context.get("__action_done", {}).keys()
        base_automation = next(iter(automation_records), None)
        res_ids = self._context.get("active_ids",
                                    [self._context.get("active_id")])

        if (
                self.model_name == "crm.lead"
                and base_automation
                and base_automation.trigger == "on_stage_set"
        ):
            crm_stage = self.env["crm.stage"].browse(
                base_automation.trg_field_ref)

            if crm_stage and crm_stage.name == "Schedule Meeting":
                leads = self.env["crm.lead"].browse(res_ids)

                # Remove existing attachments
                if self.template_id.attachment_ids:
                    self.template_id.attachment_ids.unlink()

                for lead in leads:
                    if lead.bizzup_country_id:
                        pdf_document = self.env["documents.document"].search(
                            [("name", "ilike",
                              f"{lead.bizzup_country_id.name}.pdf")],
                            limit=1
                        )
                        if pdf_document and pdf_document.datas:
                            attachment = self.env["ir.attachment"].create(
                                {
                                    "name": pdf_document.name,
                                    "type": "binary",
                                    "datas": pdf_document.datas,
                                    "res_model": "mail.template",
                                    "res_id": self.template_id.id,
                                }
                            )
                            self.template_id.attachment_ids = [
                                (4, attachment.id)]

        return super()._run_action_mail_post_multi(eval_context)
