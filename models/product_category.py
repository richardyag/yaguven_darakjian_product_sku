# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    darakjian_short_code = fields.Char(
        string="Short Code",
        help='First segment of the auto-generated Internal Reference for products in '
             'this category, e.g. "DRNG" for Diamond Rings -> "DRNG.00012345". Leave '
             'empty to skip auto-generation for this category.',
    )
