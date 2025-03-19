# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTransfer(models.Model):
    """Product Transfer"""

    _name = "product.transfer"
    _description = "Transfer Product"

    product_id = fields.Many2one("product.product", string="Product",
                                 required=True)
    location_id = fields.Many2one(
        "stock.location",
        string="From Location",
        domain="[('id', 'in', allow_bin_ids)]"
    )
    allow_bin_ids = fields.Many2many(related="product_id.allow_bins",
                                     readonly=True)
    destination_id = fields.Many2one(
        "stock.location", string="To Location",
        domain="[('id', 'in', allow_bin_ids)]"
    )
    on_hand_qty = fields.Float(
        string="On Hand Quantity", compute="_compute_on_hand_qty",
        readonly=True
    )
    qty_to_transfer = fields.Float(string="Quantity to Transfer")
    user_id = fields.Many2one(
        "res.users", string="User", default=lambda self: self.env.user
    )
    check_on_hand_qty = fields.Boolean(
        default=True, compute="_compute_check_on_hand_qty"
    )

    @api.depends("location_id", "product_id", "qty_to_transfer",
                 "on_hand_qty")
    def _compute_check_on_hand_qty(self):
        """
        Compute if the transfer button should be visible based on conditions.
        """
        for record in self:
            record.check_on_hand_qty = (
                    record.qty_to_transfer > record.on_hand_qty
                    or not record.destination_id
                    or record.on_hand_qty <= 0
            )

    @api.onchange("location_id", "destination_id")
    def _onchange_location(self):
        """
        This method checks if the from location and to location are the same.
        """
        if self.location_id and self.destination_id:
            if self.location_id == self.destination_id:
                raise ValidationError(
                    "From Location and To Location must be different."
                )

    @api.depends("product_id", "location_id")
    def _compute_on_hand_qty(self):
        """
        This method computes the on-hand quantity of a product at the
         specified location.
        """
        for record in self:
            if record.product_id and record.location_id:
                quant = self.env["stock.quant"].search(
                    [
                        ("product_id", "=", record.product_id.id),
                        ("location_id", "=", record.location_id.id),
                    ],
                    limit=1,
                )
                record.on_hand_qty = quant.quantity if quant else 0
            else:
                record.on_hand_qty = 0

    def _create_stock_move(self):
        """Create and confirm a stock move for the product transfer."""
        stock_move = self.env["stock.move"].create(
            {
                "product_id": self.product_id.id,
                "product_uom_qty": self.qty_to_transfer,
                "product_uom": self.product_id.uom_id.id,
                "location_id": self.location_id.id,
                "location_dest_id": self.destination_id.id,
                "name": "Internal Transfer",
            }
        )
        stock_move._action_confirm()
        stock_move._action_assign()
        for move_line in stock_move.move_line_ids:
            move_line.qty_done = self.qty_to_transfer
        stock_move._action_done()

    def action_transfer(self):
        """
        This method creates a stock move for the current record.
        """
        self.ensure_one()
        if self.qty_to_transfer > self.on_hand_qty:
            raise ValidationError(
                "Transfer quantity cannot exceed on-hand quantity.")

        if self.destination_id.id not in self.allow_bin_ids.ids:
            raise ValidationError(
                "Product can only be transferred to bin locations.")

        self._create_stock_move()
        self._compute_on_hand_qty()

    def action_all_transfer(self):
        """
        This method creates stock moves for all records.
        """
        records = self.search([])
        for record in records:
            if record.qty_to_transfer > record.on_hand_qty:
                raise ValidationError(
                    f"Transfer quantity for {record.product_id.name}"
                    f" cannot exceed on-hand quantity."
                )
            if (record.destination_id and
                    record.destination_id.id not in record.allow_bin_ids.ids):
                raise ValidationError(
                    f"{record.product_id.name} can only be transferred to "
                    f"bin locations."
                )
            if record.destination_id:
                record._create_stock_move()
                record._compute_on_hand_qty()
