# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Storage Bakend",
    "summary": "Implement the concept of Storage with amazon S3, sftp...",
    "version": "10.0.1.0.1",
    "category": "Storage",
    "website": "https://github.com/OCA/storage",
    "author": " Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "external_dependencies": {
        "python": [
            # "paramiko",
            # "boto",
        ]
    },
    "depends": ["base", "keychain", "component"],
    "data": [
        "views/backend_storage_view.xml",
        "data/data.xml",
        "security/ir.model.access.csv",
    ],
}
