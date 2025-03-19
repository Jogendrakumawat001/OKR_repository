# -*- coding: utf-8 -*-
# Copyright (C) Gilliam Management Services and Information Systems, Ltd. (the owner of Bizzup), 2021, 2022, 2023, 2024, 2025
# All Rights Reserved to Gilliam Management Services and Information Systems, Ltd.
# Unauthorized copying, editing or printing of this file, in any way is strictly prohibited
# Proprietary and confidential for more information, please contact
# lg@bizzup.app

from odoo import models


class StockPicking(models.Model):
    """Inherited Stock Picking"""

    _inherit = "stock.picking"

    def _process_consign_transfer(self):
        """
        Create consignment invoices and transfers.
        """
        company_a_id = 1  # ID of Company A
        is_consign_transfer = (
            self.env["ir.config_parameter"].get_param(
                "is_consign_transfer")
        )

        if not is_consign_transfer:
            return

        for record in self:
            owner_id = record.move_line_ids.filtered(
                lambda rec: rec.owner_id.id == 1)
            location_type = record.location_dest_id.usage
            if (record.state == "done" and location_type == 'customer' and
                    record.picking_type_id.code == "outgoing" and owner_id):
                invoice_obj = self.env["account.move"]
                invoice_line_obj = self.env["account.move.line"]
                picking_obj = self.env["stock.picking"]
                stock_move_line_obj = self.env["stock.move.line"]

                stock_move_company = record.company_id
                partner_in_company_a = self.env["res.partner"].sudo().search(
                    [("ref_company_ids", "in", stock_move_company.ids)],
                    limit=1
                )

                if not partner_in_company_a:
                    continue

                invoice = invoice_obj.sudo().create({
                    "partner_id": partner_in_company_a.id,
                    "move_type": "out_invoice",
                    "invoice_date": record.scheduled_date,
                    "company_id": company_a_id,
                    "narration": "חשבונית למכירות קונסיגנציה",
                })

                picking_type = self.env["stock.picking.type"].sudo().search(
                    [("company_id", "=", company_a_id),
                     ("code", "=", "outgoing")], limit=1
                )

                default_source_location = self.env[
                    "stock.location"].sudo().search(
                    [("consignation_locations", "=", True),
                     ("company_id", "=", company_a_id)], limit=1
                )

                source = (
                    partner_in_company_a.consig_location.id
                    if partner_in_company_a.consig_location
                    else default_source_location.id
                )
                new_picking = picking_obj.sudo().create({
                    "partner_id": partner_in_company_a.id,
                    "location_id": source,
                    "location_dest_id": picking_type.default_location_dest_id.id,
                    "picking_type_id": picking_type.id,
                    "company_id": company_a_id,
                    "move_type": "one",
                })
                for stock_move_line in record.move_line_ids.filtered(
                        lambda ml: ml.owner_id.id == 1):
                    product = stock_move_line.product_id
                    description = None
                    if stock_move_line.move_id.sale_line_id:
                        sale_order_name = stock_move_line.move_id.sale_line_id.order_id.name
                        description = f"SO: {sale_order_name} - Date: {stock_move_line.move_id.date}"
                    elif stock_move_line.picking_id.pos_order_id and stock_move_line.picking_id.pos_order_id.name:
                        pos_order_name = stock_move_line.picking_id.pos_order_id.name
                        description = f"POS: {pos_order_name} - Date: {stock_move_line.move_id.date}"

                    # Directly get the lot information from the stock move line itself
                    lot_name = stock_move_line.lot_id.name if stock_move_line.lot_id else None

                    invoice_line_obj.sudo().create({
                        "move_id": invoice.id,
                        "product_id": product.id,
                        "quantity": stock_move_line.quantity,
                        "price_unit": product.list_price,
                        "name": description,
                    })
                    lot_id = False
                    if lot_name:
                        lot = self.env['stock.lot'].sudo().search([
                            ('name', '=', lot_name),
                            ('product_id', '=', product.id),
                            ('company_id', '=', company_a_id)
                        ], limit=1)

                        lot_id = lot.id if lot else self.env[
                            'stock.lot'].sudo().create({
                            'name': lot_name,
                            'product_id': product.id,
                            'company_id': company_a_id,
                        }).id

                    stock_move_line_obj.sudo().create({
                        "picking_id": new_picking.id,
                        "product_id": product.id,
                        "qty_done": stock_move_line.quantity,
                        "product_uom_id": product.uom_id.id,
                        "location_id": source,
                        "location_dest_id": picking_type.default_location_dest_id.id,
                        "company_id": company_a_id,
                        'lot_id': lot_id,
                    })

                invoice.action_post()
                new_picking.action_assign()
                new_picking.button_validate()

    def button_validate(self):
        """inherit the button_validate to call _process_consign_transfer"""
        res = super(StockPicking, self).button_validate()
        self._process_consign_transfer()
        return res
