# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductProduct(models.Model):
    """Inherited the product variant to add new field"""

    _inherit = "product.product"

    allow_bins = fields.Many2many(
        "stock.location",
        string="Allowed Bins",
        required=True,
        
    )
