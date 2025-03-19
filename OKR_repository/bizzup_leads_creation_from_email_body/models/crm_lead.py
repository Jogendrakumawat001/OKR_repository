# -*- coding: utf-8 -*-
# Copyright (C) Gilliam Management Services and Information Systems, Ltd. (the owner of Bizzup), 2021, 2022, 2023, 2024, 2025
# All Rights Reserved to Gilliam Management Services and Information Systems, Ltd.
# Unauthorized copying, editing or printing of this file, in any way is strictly prohibited
# Proprietary and confidential for more information, please contact
# lg@bizzup.app

import re
import logging
from bs4 import BeautifulSoup
from odoo import models, api

_logger = logging.getLogger(__name__)


class Lead(models.Model):
    """Inherited Lead"""

    _inherit = "crm.lead"

    @api.model
    def message_new(self, msg_dict, custom_values=None):
        """inherit the message_new method to get data from email body"""
        res = super().message_new(msg_dict, custom_values)
        details = self.extract_details(msg_dict.get("body", ""))

        if details.get("name"):
            res.contact_name = details["name"]
        if details.get("telephone"):
            res.phone = details["telephone"]
        if details.get("email"):
            res.email_from = details["email"]

        return res

    def extract_details(self, message):
        """
        Extract name, email, and telephone using BeautifulSoup
        and regular expressions
        """
        soup = BeautifulSoup(message, "html.parser")

        # Extract text after specific labels, account for optional colons and spaces
        company = self.get_text_after(soup, "Company name")
        name = self.get_name_after_company(soup, company)
        telephone = self.get_text_after(soup, "Telephone")
        email = self.get_text_after(soup, "Email")

        # Handle missing or invalid names (e.g., Name: -)
        if name == "-" or not name:
            name = None

        return {
            "name": name.strip() if name else None,
            "email": email.strip() if email else None,
            "telephone": telephone.strip() if telephone else None,
        }

    def get_name_after_company(self, soup, company):
        """Get name after 'Company name' if it's present"""
        if company:
            # If company is found, find the next "Name" label after "Company name"
            name_tag = soup.find(text=re.compile(r"\bName\b", re.IGNORECASE))
            if name_tag:
                # Skip the first Name after company and look for the next Name
                next_name_tag = name_tag.find_next(
                    text=re.compile(r"\bName\b", re.IGNORECASE)
                )
                if next_name_tag:
                    return next_name_tag.find_next().text.strip()
        else:
            # If no company, find the first "Name"
            name_tag = soup.find(text=re.compile(r"\bName\b", re.IGNORECASE))
            if name_tag:
                return name_tag.find_next().text.strip()
        return None

    def get_text_after(self, soup, label):
        """Helper function to find text after a label using BeautifulSoup"""
        # Search for the label with or without a colon
        label_pattern = re.compile(rf"\b{label}\s*:?\s*", re.IGNORECASE)

        # Find the label (case-insensitive)
        tag = soup.find(text=label_pattern)
        if tag and tag.find_next():
            return tag.find_next().text.strip()
        return None
