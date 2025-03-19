# -*- coding: utf-8 -*-
from odoo import models


class StockPicking(models.Model):
    """Inherited Stock picking to create product transfer"""

    _inherit = "stock.picking"

    def button_validate(self):
        """
        override the button validate method to check id picking type incoming
        than create product transfer
        """
        res = super(StockPicking, self).button_validate()
        if self.picking_type_id.code == "incoming":
            for move_line in self.move_line_ids:
                product = move_line.product_id
                location = self.location_dest_id
                qty_received = move_line.qty_done
                if qty_received > 0:
                    self.env["product.transfer"].create(
                        {
                            "product_id": product.id,
                            "location_id": location.id,
                            "on_hand_qty": qty_received,
                        }
                    )

        return res
