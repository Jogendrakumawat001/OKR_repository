# -*- coding: utf-8 -*-
# Copyright (C) Gilliam Management Services and Information Systems, Ltd. (the owner of Bizzup), 2021, 2022, 2023, 2024, 2025
# All Rights Reserved to Gilliam Management Services and Information Systems, Ltd.
# Unauthorized copying, editing or printing of this file, in any way is strictly prohibited
# Proprietary and confidential for more information, please contact
# lg@bizzup.app

from odoo import fields, models, api


class SaleOrder(models.Model):
    """Inherited Sale Order"""

    _inherit = "sale.order"

    is_so_consig = fields.Boolean("SO Consignment")

    check_company = fields.Boolean("Check Company",
                                   compute="_compute_check_company")

    @api.depends("company_id")
    def _compute_check_company(self):
        """this method help to check sale order company to hide
        is_so_consig field"""
        for record in self:
            if record.company_id.id != 1:
                record.check_company = True
            else:
                record.check_company = False

    def action_confirm(self):
        """
        Override action_confirm to handle consignment sale orders and
        update picking destination and source locations.
        """
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            partner = order.partner_id

            # Search for default consignment location
            default_source_location = self.env["stock.location"].search(
                [
                    ("consignation_locations", "=", True),
                    ("company_id", "=", order.company_id.id),
                ],
                limit=1,
            )
            consig_location = partner.consig_location
            source_location = consig_location or default_source_location

            if (
                order.picking_ids
                and order.is_so_consig
                and source_location
            ):
                for picking in order.picking_ids:
                    location_dest_id = self.env.ref(
                        "stock.stock_location_inter_company"
                    ).id

                    # Update destination location
                    if (
                        picking.location_dest_id.usage == "customer"
                        or picking.location_dest_id.id == location_dest_id
                    ):
                        picking.write(
                            {
                                "location_dest_id": source_location.id,
                                "note": source_location.name,
                            }
                        )

                    # Update source location
                    if (
                        picking.location_id.usage == "customer"
                        or picking.location_id.id == location_dest_id
                    ):
                        picking.write({"location_id": source_location.id})

                # Match with purchase order if client reference exists
                if order.client_order_ref:
                    matching_po = (
                        self.env["purchase.order"]
                        .sudo()
                        .search(
                            [
                                ("company_id", "in", partner.ref_company_ids.ids),
                                ("name", "=", order.client_order_ref),
                            ],
                            limit=1,
                        )
                    )

                    if matching_po:
                        if not matching_po.is_po_consig:
                            matching_po.write({"is_po_consig": True})

                        # Update picking data for matching purchase order
                        for picking in matching_po.picking_ids:
                            picking.owner_id = matching_po.partner_id.id

                            # Search for consignment location
                            sub_consignation_location = (
                                self.env["stock.location"]
                                .sudo()
                                .search(
                                    [
                                        ("consignation_locations", "=", True),
                                        ("company_id", "=", picking.company_id.id),
                                    ],
                                    limit=1,
                                )
                            )
                            if sub_consignation_location:
                                picking.write(
                                    {
                                        "location_dest_id": sub_consignation_location.id,
                                        "note": sub_consignation_location,
                                    }
                                )

        return res
