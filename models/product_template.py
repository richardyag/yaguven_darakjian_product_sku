# -*- coding: utf-8 -*-
from odoo import api, models

SEQUENCE_XMLID = "yaguven_darakjian_product_sku.seq_product_sku"


class ProductTemplate(models.Model):
    """Assigns the Internal Reference right after creation, once the variant(s) exist
    and the template's category is known — safer than guessing at it from the raw
    `create()` vals, which may or may not carry `categ_id` depending on how the record
    was created."""

    _inherit = "product.template"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        config = self.env["yaguven.product.sku.config"]._get_for_company(self.env.company)
        if config.enabled:
            records._darakjian_assign_auto_sku()
        return records

    def _darakjian_assign_auto_sku(self):
        sequence = self.env.ref(SEQUENCE_XMLID, raise_if_not_found=False)
        if not sequence:
            return
        for template in self:
            short_code = template.categ_id.darakjian_short_code
            if not short_code:
                continue
            for variant in template.product_variant_ids:
                if variant.default_code:
                    continue
                variant.default_code = "%s.%s" % (short_code, sequence.next_by_id())
