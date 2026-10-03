# -*- coding: utf-8 -*-
{
    "name": "Darakjian — Auto SKU",
    "summary": "Automatic Internal Reference (SKU) generation: category code + a global sequence.",
    "description": """
Replicates, as a small native module, the SKU algorithm Darakjian already used in
Odoo 16 through a paid third-party app ("product_auto_sku" by Globalteckz) — reverse
engineered from its live configuration, not guessed:

    {category's Short Code}.{next number from one global 8-digit sequence}

e.g. "DRNG.00085941" for a Diamond Ring. No dependency on that app or any other
third-party code.

Scope, deliberately kept to what Darakjian actually uses today (the vendor-code and
attribute-code segments the old app also supported are NOT reproduced here — they were
already turned off before this was built; easy to add later if ever needed):

* A "Short Code" field on Product Category (set by hand once per category, e.g.
  "Diamond Rings" -> "DRNG").
* One company-wide on/off switch (Inventory > Configuration > Auto SKU).
* A new product only gets an auto SKU if it does not already have one — never
  overwrites a manually entered or imported Internal Reference.
* A category with no Short Code set is simply skipped (no error, no SKU assigned) —
  matches today's behavior for anything not yet configured.

The sequence starts above the highest number found anywhere in the existing catalog at
build time, so it can never collide with an already-used code, migrated or not.
""",
    "author": "Yagüven C.G.",
    "website": "https://github.com/Darakjian/yaguven_darakjian_product_sku",
    "category": "Inventory/Inventory",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["product"],
    "data": [
        "security/ir.model.access.csv",
        "data/product_sku_sequence_data.xml",
        "data/product_sku_config_data.xml",
        "views/product_category_views.xml",
        "views/product_sku_config_views.xml",
        "views/menu.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
