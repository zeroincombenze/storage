# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

try:
    from slugify import slugify
except ImportError:
    _logger.debug("Cannot `import slugify`.")


class ThumbnailMixing(models.AbstractModel):
    _name = "thumbnail.mixin"
    _description = "Thumbnail Mixin add the thumbnail capability"

    thumbnail_ids = fields.One2many(
        comodel_name="storage.thumbnail",
        string="Thumbnails",
        inverse_name="res_id",
        domain=lambda self: [("res_model", "=", self._name)],
    )
    image_medium_url = fields.Char(readonly=True)
    image_small_url = fields.Char(readonly=True)

    def _get_medium_thumbnail(self):
        return self.get_or_create_thumbnail(128, 128)

    def _get_small_thumbnail(self):
        return self.get_or_create_thumbnail(64, 64)

    def get_or_create_thumbnail(self, size_x, size_y, url_key=None):
        self.ensure_one()
        # preserve the prefetch when changing context
        self = self.with_context(bin_size=False).with_prefetch(self._prefetch)
        if url_key:
            url_key = slugify(url_key)
        thumbnail = self.env["storage.thumbnail"].browse()
        for th in self.thumbnail_ids:
            if th.size_x == size_x and th.size_y == size_y:
                if url_key and url_key != th.url_key:
                    continue
                thumbnail = th
                break
        if not thumbnail and self.data:
            vals = self.env["storage.thumbnail"]._prepare_thumbnail(
                self, size_x, size_y, url_key
            )
            # use the relation to create the thumbnail to be sure that the
            # record is added to the cache of this relation.
            self.write({"thumbnail_ids": [(0, 0, vals)]})
            return self.get_or_create_thumbnail(size_x, size_y, url_key)
        return thumbnail

    def generate_odoo_thumbnail(self):
        self.write(
            {
                "image_medium_url": self.sudo()._get_medium_thumbnail().url,
                "image_small_url": self.sudo()._get_small_thumbnail().url,
            }
        )
        return True

    @api.model
    def create(self, vals):
        record = super(ThumbnailMixing, self).create(vals)
        record.generate_odoo_thumbnail()
        return record
