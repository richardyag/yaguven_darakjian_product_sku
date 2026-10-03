# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class YaguvenProductSkuConfig(models.Model):
    """One on/off switch per company for automatic SKU generation.

    Mirrors the shape of yaguven.commission.config in the commissions module: a
    settings record Janel/Gabriel can see and toggle, found and created on demand via
    `_get_for_company` rather than hand-seeded for every company.
    """

    _name = "yaguven.product.sku.config"
    _description = "Darakjian — Auto SKU Settings"
    _order = "company_id, id"

    name = fields.Char(
        required=True,
        default=lambda self: _("Auto SKU — %s", self.env.company.name),
    )
    company_id = fields.Many2one(
        "res.company",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    active = fields.Boolean(default=True)
    enabled = fields.Boolean(
        default=True,
        help="When on, a new product without an Internal Reference gets one assigned "
             "automatically, as long as its category has a Short Code set. Never "
             "overwrites a reference entered by hand or by an import.",
    )

    @api.constrains("company_id", "active")
    def _check_single_active_per_company(self):
        for rec in self:
            if not rec.active:
                continue
            others = self.search_count([
                ("company_id", "=", rec.company_id.id),
                ("active", "=", True),
                ("id", "!=", rec.id),
            ])
            if others:
                raise ValidationError(_(
                    "Active Auto SKU settings already exist for company \"%s\". "
                    "Archive the existing one before creating another."
                ) % rec.company_id.name)

    @api.model
    def _get_for_company(self, company):
        company = company or self.env.company
        config = self.search([
            ("company_id", "=", company.id),
            ("active", "=", True),
        ], limit=1)
        if not config:
            config = self.sudo().create({
                "name": _("Auto SKU — %s", company.name),
                "company_id": company.id,
            })
        return config
