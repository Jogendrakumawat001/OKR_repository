# -*- coding: utf-8 -*-
{
    "name": "Mega Inventory Customization",
    "version": "18.0.1.0.0",
    "category": "Stock",
    "summary": "Transfer Product from one location to another",
    "depends": ["stock", "sale_management", "purchase"],
    'description': """ Includes Us-11 """,
    "data": [
        "views/product_product_view.xml",
        "security/ir.model.access.csv",
        "views/product_transfer_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mega_inventory_customization/static/src/views/**/*",
        ],
    },
    "license": "OPL-1",
    "installable": True,
    "application": False,
    "auto_install": False,
}
