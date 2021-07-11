# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    qty_delivered = fields.Float(string='Quantity Delivered', compute="calc_deliverd", translate=True)
    left_qty = fields.Float(string="Quantity Left", compute="calc_deliverd", translate=True)

    @api.depends("sale_line_ids")
    def calc_deliverd(self):
        for invoice_line in self:
            sale_order_line=invoice_line.sale_line_ids
            if sale_order_line:
                invoice_line.qty_delivered=sale_order_line.qty_delivered
                invoice_line.left_qty=sale_order_line.product_uom_qty-sale_order_line.qty_delivered

            else:
                invoice_line.qty_delivered=0.0
                invoice_line.left_qty=0.0
