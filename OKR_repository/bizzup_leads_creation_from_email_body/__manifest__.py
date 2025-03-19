# -*- coding: utf-8 -*-
# Copyright (C) Gilliam Management Services and Information Systems, Ltd. (the owner of Bizzup), 2021, 2022, 2023, 2024, 2025
# All Rights Reserved to Gilliam Management Services and Information Systems, Ltd.
# Unauthorized copying, editing or printing of this file, in any way is strictly prohibited
# Proprietary and confidential for more information, please contact
# lg@bizzup.app

{
    "name": "Bizzup Leads Creation From Email Body",
    "description": """
        US : HT01391
        This module help to extract lead email body to get name,
        email and phone values
    """,
    "version": "18.0.1.0.0",
    "category": "",
    "license": "Other proprietary",
    "author": "Gilliam Management Services and Information Systems, Ltd.",
    "website": "www.bizzup.app",
    "depends": ["crm"],
    "external_dependencies": {
        "python": ["beautifulsoup4"],
    },
    "installable": True,
    "application": False,
}
