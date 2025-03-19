# -*- coding: utf-8 -*-
# Copyright (C) Gilliam Management Services and Information Systems, Ltd. (the owner of Bizzup), 2021, 2022, 2023, 2024, 2025
# All Rights Reserved to Gilliam Management Services and Information Systems, Ltd.
# Unauthorized copying, editing or printing of this file, in any way is strictly prohibited
# Proprietary and confidential for more information, please contact
# lg@bizzup.app

{
    "name": "Bizzup Event Customization",
    "description": """
     US : HT01424
     Check event feedback handling.
     """,
    "version": "18.0.1.2.2",
    "license": "Other proprietary",
    "author": "Gilliam Management Services and Information Systems, Ltd.",
    "website": "https://bizzup.app",
    "depends": ["website", "sale_management", "event", "crm",
                "bizzup_crm_customization"],
    "data": [
        "security/ir.model.access.csv",
        "views/event_event_views.xml",
        "views/chef_answer_view.xml",
        "views/crm_lead_view.xml",
        "views/website_template_view.xml",
    ],
    "application": True,
    "installable": True,
}
